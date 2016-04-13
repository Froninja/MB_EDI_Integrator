# -*- mode: python -*-

block_cipher = None


a = Analysis(['launcher.py'],
             pathex=['C:\\Users\\Jacob\\Documents\\Visual Studio 2013\\Projects\\MB_EDI_Integrator'],
             binaries=[('C:\\Python34\\Lib\\site-packages\\PyQt5\\plugins\\printsupport\\windowsprintersupport.dll','qt5_plugins\\printsupport')],
             datas=[('config.txt','.'),('PO_Database','.'),('shipping_analysis.csv','.'),('Destlog.csv','.'),('Desclog.csv','.'),
                    ('UPC_Exception.csv','.'),('Resources\*.png','Resources'),('Resources\*.bmp','Resources'),
                    ('OutputTemplates\*.txt','OutputTemplates')],
             hiddenimports=['_mssql','decimal'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='launcher',
          debug=True,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='launcher')
