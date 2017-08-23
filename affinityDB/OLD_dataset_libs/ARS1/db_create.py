    elif FLAGS.action == 'binding_affinity':
        if FLAGS.param is None:
            raise Exception('param required')

        bind_param = FLAGS.param
        if not bind_param in config.bind_pm.keys():
            raise Exception('No binidng affinity file for key {} in config\n'.format(bind_param)\
                             + 'Available choices are {}'.format(str(config.bind_pm.keys())))

        
        table_param = {
            'func':'binding_affinity',
            'bind_param': config.bind_pm[bind_param]
        }
