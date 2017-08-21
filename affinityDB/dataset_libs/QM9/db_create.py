

    elif FLAGS.action == 'local_qm9_load':
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")

        folder_name = FLAGS.folder_name
        table_param = {
            'func':'local_qm9_load',
            'output_folder': folder_name,
