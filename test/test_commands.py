from pylsp_rope.plugin import pylsp_commands


def test_command_registration(config, workspace):
    commands = pylsp_commands(config, workspace)

    assert isinstance(commands, list)
    assert all(isinstance(cmd, str) for cmd in commands)
    assert all(cmd.startswith("pylsp_rope.") for cmd in commands)
