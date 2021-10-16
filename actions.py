
def action_handler(action, parameters, return_var, game):
    return_values = {}
    if action == 'iniciar':
        return_values = game.start()

    elif action == 'mais1carta':
        return_values = game.draw_card()

    elif action == 'parar':
        return_values = game.evaluate()
        game.terminate()


    elif action == 'estatística':
        return_values = game.stats()


    return {
            'skills': {
                'main skill': {
                    'user_defined': { return_var: return_values}
                }
            }
        }




