from player_interaction import PlayerAI
import time

player_ai = PlayerAI()

action_input = int(input('Select an action: '))

for i in list(range(2))[::-1]:
    print(i+1)
    time.sleep(1)

player_ai.action(choice=action_input)