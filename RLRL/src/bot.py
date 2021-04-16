from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3
from random import random
from ddpg import DDPG
import numpy as np
class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.boost_pad_tracker = BoostPadTracker()
        self.previous_Goals = 0
        self.previous_my_Goals = 0
        self.previous_enemy_Goals = 0
        self.DDPG = None
    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        self.boost_pad_tracker.initialize_boosts(self.get_field_info())


    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """

        # Keep our boost pad info updated with which pads are currently active
        self.boost_pad_tracker.update_boost_status(packet)

        # Gather some information about our car and the ball
        my_car = packet.game_cars[self.index]

        if self.team == 0:
            goal_location = np.array((0, 5213, 321.3875))
        else:
            goal_location = np.array((0, -5213, 321.3875))
        def dictToArr(d):
            return np.array((d.x,d.y,d.z))
        field_length = 10426
        max_velocity = 1000
        ball_velocity = dictToArr(packet.game_ball.physics.velocity)
        car_location = dictToArr(my_car.physics.location)
        car_velocity = dictToArr(my_car.physics.velocity)
        ball_location = dictToArr(packet.game_ball.physics.location)
        car_ball = ball_location - car_location
        ball_goal = goal_location - ball_location
        
        my_Goals = packet.teams[self.team].score
        enemy_goals = packet.teams[1-self.team].score
        current_Goals =  my_Goals+enemy_goals
        print("velocity: ", car_velocity, end = " ")
        state = np.concatenate((car_ball[:2]/field_length,ball_goal[:2]/field_length,car_velocity[:2]/max_velocity,ball_velocity[:2]/max_velocity))

        if self.DDPG is None:
            self.DDPG = DDPG(state)
        reward = 0.0

        #denom = np.linalg.norm(ball_goal) * np.linalg.norm(ball_velocity) 
        #if denom != 0:
        reward += np.dot(ball_goal, ball_velocity)
            #np.arccos(np.dot(ball_goal, ball_velocity)/denom)

        #denom = np.linalg.norm(car_ball) * np.linalg.norm(car_velocity)

        #if denom != 0:
        reward += np.dot(car_ball, car_velocity)

            #100*np.arccos(np.dot(car_ball, car_velocity)/denom)
        
        #if denom != 0:
        #reward += 2000/np.linalg.norm(car_ball)


        if my_Goals != self.previous_my_Goals:
            reward = 1000
        if enemy_goals != self.previous_enemy_Goals:
            reward = -1000

        print("Time: ", round(packet.game_info.seconds_elapsed,2), end = " ")
        action = self.DDPG.step(state, reward)


        if current_Goals != self.previous_Goals:
            self.DDPG.newEpisode()


        self.previous_Goals = current_Goals
        self.previous_enemy_Goals = enemy_goals
        self.previous_my_Goals = my_Goals

        #target_location = ball_location

        # if car_location.dist(ball_location) > 500:
        #     # We're far away from the ball, let's try to lead it a little bit
        #     ball_prediction = self.get_ball_prediction_struct()  # This can predict bounces, etc
        #     ball_in_future = find_slice_at_time(ball_prediction, packet.game_info.seconds_elapsed + 1)

        #     # ball_in_future might be None if we don't have an adequate ball prediction right now, like during
        #     # replays, so check it to avoid errors.
        #     if ball_in_future is not None:
        #         target_location = Vec3(ball_in_future.physics.location)
        #         self.renderer.draw_line_3d(ball_location, target_location, self.renderer.cyan())

        # Draw some things to help understand what the bot is thinking
        # self.renderer.draw_line_3d(car_location, target_location, self.renderer.white())
        # self.renderer.draw_string_3d(car_location, 1, 1, f'Speed: {car_velocity.length():.1f}', self.renderer.white())
        # self.renderer.draw_rect_3d(target_location, 8, 8, True, self.renderer.cyan(), centered=True)



        controls = SimpleControllerState()
        
        
        controls.steer = action[0]
        controls.throttle = action[1]
        controls.boost = action[2]>0
        # You can set more controls if you want, like controls.boost.

        return controls