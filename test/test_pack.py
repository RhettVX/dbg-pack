from DbgPack import Pack


def test_load_pack():
    pack = Pack("sample.pack")
    assert len(pack) == 235
    assert pack.path == "sample.pack"


def test_load_asset():
    pack = Pack("sample.pack")
    asset1 = pack['AbilityClasses.txt']
    assert asset1.asset_type == 'txt'
    assert asset1.offset == 8192
    assert len(asset1) == 149
    assert asset1.crc32 == 1748740018
    
    asset2 = pack['Contrails_Vortex_Purple.xml']
    assert asset2.asset_type == 'xml'
    assert asset2.offset == 770682
    assert len(asset2) == 2563
    assert asset2.crc32 == 4092021062
