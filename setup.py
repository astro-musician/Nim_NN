from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['numpy'], 'excludes': []}

base = 'gui'

executables = [
    Executable('game.py', base=base, target_name = 'test-game-NN')
]

setup(name='test-game-NN',
      version = '1.0',
      description = 'Testing nim game as an executable',
      options = {'build_exe': build_options},
      executables = executables)
