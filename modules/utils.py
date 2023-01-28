import json
import requests

from PIL import Image
from config import ASSET, MASTER_DB


def get_card_thumbnail_url(asset_bundle_name, special_training=False):
    if special_training:
        return f"{ASSET}/character/member_cutout/{asset_bundle_name}/after_training/thumbnail_xl.png"
    else:
        return f"{ASSET}/character/member_cutout/{asset_bundle_name}/normal/thumbnail_xl.png"


def generate_honor(honor, is_main=True):
    star = False
    background_asset_bundle_name = ''
    asset_bundle_name = ''
    group_id = 0
    honor_rarity = 0
    honor_type = ''

    try:
        honor['profileHonorType']
    except:
        honor['profileHonorType'] = 'normal'
        
    if honor['profileHonorType'] == 'normal':  # 普通牌子
        honors = requests.get(url=f'{MASTER_DB}/honors.json').json()
        honor_groups = requests.get(url=f'{MASTER_DB}/honorGroups.json').json()

        for _honor in honors:
            if _honor['id'] == honor['honorId']:
                asset_bundle_name = _honor['assetbundleName']
                group_id = _honor['groupId']
                honor_rarity = _honor['honorRarity']
                try:
                    level2 = _honor['levels'][1]['level']
                    star = True
                except IndexError:
                    pass
                for honor_group in honor_groups:
                    if honor_group['id'] == _honor['groupId']:
                        try:
                            background_asset_bundle_name = honor_group['backgroundAssetbundleName']
                        except KeyError:
                            background_asset_bundle_name = ''
                        honor_type = honor_group['honorType']
                        break

        filename = 'honor'
        main_name = 'rank_main.png'
        sub_name = 'rank_sub.png'
        degree_main_name = 'degree_main.png'
        degree_sub_name = 'degree_sub.png'

        if honor_type == 'rank_match':
            filename = 'rank_live/honor'
            main_name = 'main/main.png'
            sub_name = 'sub/sub.png'
            degree_main_name = 'degree_main/degree_main.png'
            degree_sub_name = 'degree_sub/degree_sub.png'

        if is_main:  # 大图
            if honor_rarity == 'low':
                frame = Image.open('pictures/frames/frame_degree_m_1.png')
            elif honor_rarity == 'middle':
                frame = Image.open('pictures/frames/frame_degree_m_2.png')
            elif honor_rarity == 'high':
                frame = Image.open('pictures/frames/frame_degree_m_3.png')
            else:
                frame = Image.open('pictures/frames/frame_degree_m_4.png')

            if background_asset_bundle_name == '':
                rank_pic = None
                pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{asset_bundle_name}/{degree_main_name}', stream=True).raw)
                try:
                    rank_pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{asset_bundle_name}/{main_name}', stream=True).raw)
                except:
                    pass
                r, g, b, mask = frame.split()
                if honor_rarity == 'low':
                    pic.paste(frame, (8, 0), mask)
                else:
                    pic.paste(frame, (0, 0), mask)
                if rank_pic is not None:
                    r, g, b, mask = rank_pic.split()
                    pic.paste(rank_pic, (190, 0), mask)
            else:
                pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{background_asset_bundle_name}/{degree_main_name}', stream=True).raw)
                rank_pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{asset_bundle_name}/{main_name}', stream=True).raw)
                r, g, b, mask = frame.split()
                if honor_rarity == 'low':
                    pic.paste(frame, (8, 0), mask)
                else:
                    pic.paste(frame, (0, 0), mask)
                r, g, b, mask = rank_pic.split()
                pic.paste(rank_pic, (190, 0), mask)

            if honor_type == 'character' or honor_type == 'achievement':
                if star is True:
                    honor_level = honor['honorLevel']
                    if honor_level > 10:
                        honor_level = honor_level - 10
                    if honor_level < 5:
                        for i in range(0, honor_level):
                            lv = Image.open('pictures/icons/icon_degreeLv.png')
                            r, g, b, mask = lv.split()
                            pic.paste(lv, (54 + 16 * i, 63), mask)
                    else:
                        for i in range(0, 5):
                            lv = Image.open('pictures/icons/icon_degreeLv.png')
                            r, g, b, mask = lv.split()
                            pic.paste(lv, (54 + 16 * i, 63), mask)
                        for i in range(0, honor_level - 5):
                            lv = Image.open('pictures/icons/icon_degreeLv6.png')
                            r, g, b, mask = lv.split()
                            pic.paste(lv, (54 + 16 * i, 63), mask)

        else:  # 小图
            if honor_rarity == 'low':
                frame = Image.open('pictures/frames/frame_degree_s_1.png')
            elif honor_rarity == 'middle':
                frame = Image.open('pictures/frames/frame_degree_s_2.png')
            elif honor_rarity == 'high':
                frame = Image.open('pictures/frames/frame_degree_s_3.png')
            else:
                frame = Image.open('pictures/frames/frame_degree_s_4.png')

            if background_asset_bundle_name == '':
                rank_pic = None
                pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{asset_bundle_name}/{degree_sub_name}', stream=True).raw)
                try:
                    rank_pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{asset_bundle_name}/{sub_name}', stream=True).raw)
                except:
                    pass
                r, g, b, mask = frame.split()
                if honor_rarity == 'low':
                    pic.paste(frame, (8, 0), mask)
                else:
                    pic.paste(frame, (0, 0), mask)
                if rank_pic is not None:
                    r, g, b, mask = rank_pic.split()
                    pic.paste(rank_pic, (34, 42), mask)
            else:
                pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{background_asset_bundle_name}/{degree_sub_name}', stream=True).raw)
                rank_pic = Image.open(requests.get(url=f'{ASSET}/{filename}/{asset_bundle_name}/{sub_name}', stream=True).raw)
                r, g, b, mask = frame.split()
                if honor_rarity == 'low':
                    pic.paste(frame, (8, 0), mask)
                else:
                    pic.paste(frame, (0, 0), mask)
                r, g, b, mask = rank_pic.split()
                pic.paste(rank_pic, (34, 42), mask)

            if honor_type == 'character' or honor_type == 'achievement':
                if star is True:
                    honor_level = honor['honorLevel']
                    if honor_level > 10:
                        honor_level = honor_level - 10
                    if honor_level < 5:
                        for i in range(0, honor_level):
                            lv = Image.open('pictures/icons/icon_degreeLv.png')
                            r, g, b, mask = lv.split()
                            pic.paste(lv, (54 + 16 * i, 63), mask)
                    else:
                        for i in range(0, 5):
                            lv = Image.open('pictures/icons/icon_degreeLv.png')
                            r, g, b, mask = lv.split()
                            pic.paste(lv, (54 + 16 * i, 63), mask)
                        for i in range(0, honor_level - 5):
                            lv = Image.open('pictures/icons/icon_degreeLv6.png')
                            r, g, b, mask = lv.split()
                            pic.paste(lv, (54 + 16 * i, 63), mask)

    elif honor['profileHonorType'] == 'bonds':  # CP牌子
        bonds_honors = requests.get(url=f'{MASTER_DB}/bondsHonors.json').json()

        for i in bonds_honors:
            if i['id'] == honor['honorId']:
                game_character_unit_id1 = i['gameCharacterUnitId1']
                game_character_unit_id2 = i['gameCharacterUnitId2']
                honor_rarity = i['honorRarity']
                break

        if is_main:  # 大图
            if honor['bondsHonorViewType'] == 'reverse':
                pic = get_bonds_background(game_character_unit_id2, game_character_unit_id1)
            else:
                pic = get_bonds_background(game_character_unit_id1, game_character_unit_id2)

            chara1 = Image.open(f'pictures/chara/chr_sd_{str(game_character_unit_id1).zfill(2)}_01/chr_sd_'
                                f'{str(game_character_unit_id1).zfill(2)}_01.png')
            chara2 = Image.open(f'pictures/chara/chr_sd_{str(game_character_unit_id2).zfill(2)}_01/chr_sd_'
                                f'{str(game_character_unit_id2).zfill(2)}_01.png')

            if honor['bondsHonorViewType'] == 'reverse':
                chara1, chara2 = chara2, chara1

            r, g, b, mask = chara1.split()
            pic.paste(chara1, (0, -40), mask)
            r, g, b, mask = chara2.split()
            pic.paste(chara2, (220, -40), mask)
            mask_img = Image.open('pictures/masks/mask_degree_main.png')
            r, g, b, mask = mask_img.split()
            pic.putalpha(mask)

            if honor_rarity == 'low':
                frame = Image.open('pictures/frames/frame_degree_m_1.png')
            elif honor_rarity == 'middle':
                frame = Image.open('pictures/frames/frame_degree_m_2.png')
            elif honor_rarity == 'middle':
                frame = Image.open('pictures/frames/frame_degree_m_3.png')
            else:
                frame = Image.open('pictures/frames/frame_degree_m_4.png')

            r, g, b, mask = frame.split()

            if honor_rarity == 'low':
                pic.paste(frame, (8, 0), mask)
            else:
                pic.paste(frame, (0, 0), mask)

            word_bundle_name = f"honorname_{str(game_character_unit_id1).zfill(2)}" \
                               f"{str(game_character_unit_id2).zfill(2)}_{str(honor['bondsHonorWordId'] % 100).zfill(2)}_01"
            word = Image.open(requests.get(url=f'{ASSET}/bonds_honor/word/{word_bundle_name}/{word_bundle_name}.png', stream=True).raw)
            r, g, b, mask = word.split()
            pic.paste(word, (int(190 - (word.size[0] / 2)), int(40 - (word.size[1] / 2))), mask)

            if honor['honorLevel'] < 5:
                for i in range(0, honor['honorLevel']):
                    lv = Image.open('pictures/icons/icon_degreeLv.png')
                    r, g, b, mask = lv.split()
                    pic.paste(lv, (54 + 16 * i, 63), mask)
            else:
                for i in range(0, 5):
                    lv = Image.open('pictures/icons/icon_degreeLv.png')
                    r, g, b, mask = lv.split()
                    pic.paste(lv, (54 + 16 * i, 63), mask)
                for i in range(0, honor['honorLevel'] - 5):
                    lv = Image.open('pictures/icons/icon_degreeLv6.png')
                    r, g, b, mask = lv.split()
                    pic.paste(lv, (54 + 16 * i, 63), mask)

        else:  # 小图
            if honor['bondsHonorViewType'] == 'reverse':
                pic = get_bonds_background(game_character_unit_id2, game_character_unit_id1, False)
            else:
                pic = get_bonds_background(game_character_unit_id1, game_character_unit_id2, False)
            chara1 = Image.open(f'pictures/chara/chr_sd_{str(game_character_unit_id1).zfill(2)}_01/chr_sd_'
                                f'{str(game_character_unit_id1).zfill(2)}_01.png')
            chara2 = Image.open(f'pictures/chara/chr_sd_{str(game_character_unit_id2).zfill(2)}_01/chr_sd_'
                                f'{str(game_character_unit_id2).zfill(2)}_01.png')

            if honor['bondsHonorViewType'] == 'reverse':
                chara1, chara2 = chara2, chara1

            chara1 = chara1.resize((120, 102))
            r, g, b, mask = chara1.split()
            pic.paste(chara1, (-5, -20), mask)
            chara2 = chara2.resize((120, 102))
            r, g, b, mask = chara2.split()
            pic.paste(chara2, (60, -20), mask)
            mask_img = Image.open('pictures/masks/mask_degree_sub.png')
            r, g, b, mask = mask_img.split()
            pic.putalpha(mask)

            if honor_rarity == 'low':
                frame = Image.open('pictures/frames/frame_degree_s_1.png')
            elif honor_rarity == 'middle':
                frame = Image.open('pictures/frames/frame_degree_s_2.png')
            elif honor_rarity == 'middle':
                frame = Image.open('pictures/frames/frame_degree_s_3.png')
            else:
                frame = Image.open('pictures/frames/frame_degree_s_4.png')
            r, g, b, mask = frame.split()

            if honor_rarity == 'low':
                pic.paste(frame, (8, 0), mask)
            else:
                pic.paste(frame, (0, 0), mask)

            if honor['honorLevel'] < 5:
                for i in range(0, honor['honorLevel']):
                    lv = Image.open('pictures/icons/icon_degreeLv.png')
                    r, g, b, mask = lv.split()
                    pic.paste(lv, (54 + 16 * i, 63), mask)
            else:
                for i in range(0, 5):
                    lv = Image.open('pictures/icons/icon_degreeLv.png')
                    r, g, b, mask = lv.split()
                    pic.paste(lv, (54 + 16 * i, 63), mask)
                for i in range(0, honor['honorLevel'] - 5):
                    lv = Image.open('pictures/icons/icon_degreeLv6.png')
                    r, g, b, mask = lv.split()
                    pic.paste(lv, (54 + 16 * i, 63), mask)

    pic.save(fp='test.png', format='png')

    return pic


def get_bonds_background(chara1, chara2, ismain=True):
    if ismain:
        pic1 = Image.open(f'pictures/bonds/{str(chara1)}.png')
        pic2 = Image.open(f'pictures/bonds/{str(chara2)}.png')
        pic2 = pic2.crop((190, 0, 380, 80))
        pic1.paste(pic2, (190, 0))
    else:
        pic1 = Image.open(f'pictures/bonds/{str(chara1)}_sub.png')
        pic2 = Image.open(f'pictures/bonds/{str(chara2)}_sub.png')
        pic2 = pic2.crop((90, 0, 380, 80))
        pic1.paste(pic2, (90, 0))
    return pic1