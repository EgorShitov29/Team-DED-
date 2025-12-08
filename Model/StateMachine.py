from statemachine import State, StateMachine


class GameplayStateMachine(StateMachine):
    enter_to_dungeon = State('enter_to_dungeon', initial=True)
    select_level = State('select_level')
    squad_build = State('squad_build')
    activate_dungeon = State('activate_dungeon')
    battle = State('battle')

    to_select_level = enter_to_dungeon.to(select_level)
    to_squad_build = select_level.to(squad_build)
    to_activate_dungeon = squad_build.to(activate_dungeon)
    to_batlle = activate_dungeon.to(battle)