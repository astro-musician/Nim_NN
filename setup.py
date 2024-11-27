from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('train.py', base=base, target_name = 'test-training-NN')
]

setup(name='test-training-NN',
      version = '1.0',
      description = 'Testing nim game as an executable',
      options = {'build_exe': build_options},
      executables = executables)
