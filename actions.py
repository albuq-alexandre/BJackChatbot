
def action_handler(action, parameters, return_var, game, audible):
    return_values = {}
    return_values_img = None

    if action == 'iniciar':
        txt_values, return_values_img = game.start(audible)
        return_values["text"] = txt_values
        return_values["img"] = return_values_img if not audible else None


    elif action == 'mais1carta':
        txt_values, return_values_img = game.draw_card(audible)
        return_values["text"] = txt_values
        return_values["img"] = return_values_img if not audible else None

    elif action == 'parar':
        if game.running:
            game.dealers_turn(audible)
        txt_values, return_values_img = game.evaluate(audible)
        return_values["text"] = txt_values
        return_values["img"] = return_values_img if not audible else None


    elif action == 'terminar':
        ret = ''
        for player in game.players:
            ret = ret + "<b>" + player.name + "</b>\n"
            ret = ret + player.list_matches() + '\n'
            ret = ret + player.stats() + '\n'
        return_values["text"] = ret
        game.terminate()

    elif action == 'listar':
        return_values["text"] = game.players[1].list_matches()

    elif action == 'estatística':
        return_values["text"] = game.players[1].stats()




    return {
            'skills': {
                'main skill': {
                    'user_defined': { return_var: return_values }

                }
            }
        }




