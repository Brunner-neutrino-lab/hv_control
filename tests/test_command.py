from hv_control.command import GetSetCommand

def test_command():
    outputSwitch = GetSetCommand('outputSwitch', int)
    outputSwitch('0.0.0.0', 'u0')
    outputSwitch('0.0.0.0', 'u0', 1)