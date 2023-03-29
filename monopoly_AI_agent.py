import numpy as np
from monopoly_classes import DoubleDice

class AI_Agent_MinMax:
  def __init__(self, depth=4):
      self.depth = depth

  def move(self, player, properties, players):
      """
      Choose the optimal action for a player in a Monopoly game 
      using the ExpectMinMax algorithm. Here the agent plays to 
      maximize its profits.
      """
      actions = self.get_legal_moves(player, properties)
      _, action = self.expectimax_decision(player, properties, players, 0, True)
      assert action in actions
      self.do_action(player, properties, action, players)

  def expectimax_decision(self, player, properties, players, depth, maximizing_player):
      """
      Returns the optimal action to take for a player using 
      the Expectimax algorithm.
      """
      if player.is_bankrupt():
          return -np.inf, None
      
      if depth == self.depth:
          return self.calc_board_utility(player, properties), None

      if maximizing_player:
          v_max = -np.inf
          best_action = None
          for action in self.get_legal_moves(player, properties):
              copy_player = player.copy()
              copy_properties = self.get_copy_properties(properties)
              copy_players = self.get_copy_players(players)
              self.do_action(copy_player, copy_properties, action, copy_players)
              v, _ = self.expectimax_decision(copy_player, copy_properties, copy_players, depth + 1, False)
              if v > v_max:
                  v_max, best_action = v, action
          return v_max, best_action
          
      else:
          v_exp = 0
          actions = self.get_legal_moves(player, properties)
          for action in actions:
              copy_player = player.copy()
              copy_properties = self.get_copy_properties(properties)
              copy_players = self.get_copy_players(players)
              self.do_action(copy_player, copy_properties, action, copy_players)
              v, _ = self.expectimax_decision(copy_player, copy_properties, copy_players, depth + 1, True)
              v_exp += v / len(actions)
          return v_exp, None
      
  def get_legal_moves(self, player, properties):
      """
      Returns all legal moves for a player in a Monopoly game.
      """
      moves = []
      dices = DoubleDice()
      d1, d2, roll_result = dices.roll_double_dice()  
      if player.jail and player.jail_cards > 0:
          moves.append('use jail card')
      elif player.jail:
          moves.append('do nothing')
      else:
          moves.append('end turn')
          if d1 == d2:
              moves.append('roll dice again')
              if player.doubles_rolls < 2:
                  moves.append('move')
          else:
              moves.append('move')
      return moves

  def do_action(self, player, properties, action, players):
      """
      Performs the given action for the agent. Here agent 
      receives utility for moving to other tiles and receives 
      rewards for collecting rent for its owned tiles.
      """
      if action == 'use jail card' and player.jail_cards > 0:
          player.jail = False
          player.jail_cards -= 1
      elif action == 'do nothing':
          player.jail_turns += 1
      elif action == 'end turn':
          player.jail_turns = max(0, player.jail_turns - 1)
      elif action == 'move':
          dices = DoubleDice()
          d1, d2, roll_result = dices.roll_double_dice()  
          player.move(roll_result)
          if properties[player.position].owner and properties[player.position].owner != player:
              player.pay_rent(properties[player.position])
          elif player.money > properties[player.position].price * 1.1:
              player.buy_property(properties[player.position])
      elif action == 'roll dice again':
          player.move(d1+d2)
          player.doubles_rolls += 1
          if properties[player.position].owner and properties[player.position].owner != player:
              player.pay_rent(properties[player.position])
          elif player.money > properties[player.position].price * 1.1:
              player.buy_property(properties[player.position])
      else:
          raise Exception('Invalid action')

  def calc_board_utility(self, player, properties):
      """
      Evaluates the game utility for each player in a game. Here the agent 
      evaluates the sum of its tile property values minus the sum of its 
      players debts.
      """
      utility = 0
      for p in properties:
          if p.owner == player:
              utility += p.price
      utility -= player.get_debt()
      return utility
  
  def get_copy_properties(self, properties):
      """
      Returns a deepcopy of a list of properties.
      """
      copy_properties = []
      for p in properties:
          copy_properties.append(p.copy())
      return copy_properties

  def get_copy_players(self, players):
      """
      Returns a deepcopy of a list of players.
      """
      copy_players = []
      for player in players:
          copy_players.append(player.copy())
      return copy_players
