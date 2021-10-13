from game import BlackJackGame


def action_handler(action, parameters, return_var):
    return_values = {}
    game = None
    if action == 'iniciar':
        if not game:
            game = BlackJackGame()
        return_values = game.start()

    elif action == 'mais1carta':
        return_values = game.draw_card()

    elif action == 'parar':
        return_values = game.evaluate()
        game = None

    elif action == 'estatística':
        return_values = game.stats()


    return {
            'skills': {
                'main skill': {
                    'user_defined': { return_var: return_values}
                }
            }
        }




