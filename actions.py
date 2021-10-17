
def action_handler(action, parameters, return_var, game):
    return_values = {}
    if action == 'iniciar':
        return_values = game.start()

    elif action == 'mais1carta':
        return_values = game.draw_card()

    elif action == 'parar':
        if game.running:
            game.dealers_turn()
        return_values = game.evaluate()

    elif action == 'terminar':
        ret = ''
        for player in game.players:
            ret = ret + "<b>" + player.name + "</b>\n"
            ret = ret + player.list_matches() + '\n'
            ret = ret + player.stats() + '\n'
        return_values = ret
        game.terminate()

    elif action == 'listar':
        return_values = game.players[1].list_matches()

    elif action == 'estatística':
        return_values = game.players[1].stats()


    return_values_img = None

    return {
            'skills': {
                'main skill': {
                    'user_defined': { return_var: return_values},
                    'user_image': { 'img_resposta': return_values_img}
                }
            }
        }




