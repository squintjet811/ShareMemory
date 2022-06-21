from setuptools import setup, find_packages


setup(name = 'ShareMemory',
      version = '0.1' ,
      descroption = 'The light weight share memory for inter process communication',
      url = 'https://github.com/squintjet811/ShareMemory',
      author = 'squintjet811',
      author_email = 'squintjet811@gmail.com',
      license = 'MIT',
      packages = find_packages("src"),
      install_requires = ['numpy == 1.22.0'],
      package_data = {
           'doc' :['*.txt'] ,
           'memorymapfile' : ['*.txt'] ,
            '' : ['*.md'],
      },

      #include_package_data = True,

      zip_safe = False)


