import sys
sys.path.insert(1, './source')
import _scrape_engl393
from spell import Spell


# def test_engl393_regex():
#     test_str = """9th-level conjuration
# Casting Time: 1 action
# Range: Self
# Components: V, S, M
# Duration: Instantaneous
# Wish is the mightiest spell a mortal creature can cast. By simply speaking aloud, you can alter the very foundations of reality in accord with your desires.
# The basic use of this spell is to duplicate any other spell of or lower. You don't need to meet any requirements in that spell, including costly components. The spell simply takes effect. Alternatively, you can create one of the following effects of your choice.
# • You create one object of up to 25,000 gp in value that isn't a magic item. The object can be no more than 300 feet in any dimension, and it appears in an unoccupied space you can see on the ground.
# • You allow up to twenty creatures that you can see to regain all hit points, and you end all effects on them described in the greater restoration spell.
# • You grant up to ten creatures that you can see resistance to a damage type you choose.
# • You grant up to ten creatures you can see immunity to a single spell or other magical effect for 8 hours. For instance, you could make yourself and all your companions immune to a lich's life drain attack.
# • You undo a single recent event by forcing a reroll of any roll made within the last round (including your last turn). Reality reshapes itself to accommodate the new result. For example, a wish spell could undo an opponent's successful save, a foe's critical hit, or a friend's failed save. You can force the reroll to be made with advantage or disadvantage, and you can choose whether to use the reroll or the original roll.
# You might be able to achieve something beyond the scope of the above examples. State your wish to the DM as precisely as possible. The DM has great latitude in ruling what occurs in such an instance, the greater the wish, the greater the likelihood that something goes wrong. This spell might simply fail, the effect you desire might only be partly achieved, or you might suffer some unforeseen consequence as a result of how you worded the wish. For example, wishing that a villain were dead might propel you forward in time to a period when that villain is no longer alive, effectively removing you from the game. Similarly, wishing for a legendary magic item or artifact might instantly transport you to the presence of the item's current owner.
# The stress of casting this spell to produce any effect other than duplicating another spell weakens you. After enduring that stress, each time you cast a spell until you finish a long rest, you take 1d10 necrotic damage per level of that spell. This damage can't be reduced or prevented in any way. In addition, your Strength drops to 3, if it isn't 3 or lower already, for 2d4 days. For each of those days that you spend resting and doing nothing more than light activity, your remaining recovery time decreases by 2 days. Finally, there is a 33 percent chance that you are unable to cast wish ever again if you suffer this stress."""
#     info = _scrape_engl393.parse_info(test_str)
#     assert info['level_and_type'] == "9th-level conjuration"
#     assert info['cast_time'] == "1 action"
#     assert info['range'] == 'Self'
#     assert info['components'] == 'V, S, M'
#     assert info['duration'] == 'Instantaneous'
#     assert info['descr_n'] == """Wish is the mightiest spell a mortal creature can cast. By simply speaking aloud, you can alter the very foundations of reality in accord with your desires.
# The basic use of this spell is to duplicate any other spell of or lower. You don't need to meet any requirements in that spell, including costly components. The spell simply takes effect. Alternatively, you can create one of the following effects of your choice.
# • You create one object of up to 25,000 gp in value that isn't a magic item. The object can be no more than 300 feet in any dimension, and it appears in an unoccupied space you can see on the ground.
# • You allow up to twenty creatures that you can see to regain all hit points, and you end all effects on them described in the greater restoration spell.
# • You grant up to ten creatures that you can see resistance to a damage type you choose.
# • You grant up to ten creatures you can see immunity to a single spell or other magical effect for 8 hours. For instance, you could make yourself and all your companions immune to a lich's life drain attack.
# • You undo a single recent event by forcing a reroll of any roll made within the last round (including your last turn). Reality reshapes itself to accommodate the new result. For example, a wish spell could undo an opponent's successful save, a foe's critical hit, or a friend's failed save. You can force the reroll to be made with advantage or disadvantage, and you can choose whether to use the reroll or the original roll.
# You might be able to achieve something beyond the scope of the above examples. State your wish to the DM as precisely as possible. The DM has great latitude in ruling what occurs in such an instance, the greater the wish, the greater the likelihood that something goes wrong. This spell might simply fail, the effect you desire might only be partly achieved, or you might suffer some unforeseen consequence as a result of how you worded the wish. For example, wishing that a villain were dead might propel you forward in time to a period when that villain is no longer alive, effectively removing you from the game. Similarly, wishing for a legendary magic item or artifact might instantly transport you to the presence of the item's current owner.
# The stress of casting this spell to produce any effect other than duplicating another spell weakens you. After enduring that stress, each time you cast a spell until you finish a long rest, you take 1d10 necrotic damage per level of that spell. This damage can't be reduced or prevented in any way. In addition, your Strength drops to 3, if it isn't 3 or lower already, for 2d4 days. For each of those days that you spend resting and doing nothing more than light activity, your remaining recovery time decreases by 2 days. Finally, there is a 33 percent chance that you are unable to cast wish ever again if you suffer this stress."""


def test_from_engl393():
    test_info = {
        'level_and_type': "1st-level divination",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S",
        'duration': "30 minutes",
        'descr_n': "This is my description",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description"
    assert spell.AtHigherLevels == ""
    assert spell.Ritual == False


def test_from_engl393_ritual():
    test_info = {
        'level_and_type': "1st-level (ritual) divination",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S",
        'duration': "30 minutes",
        'descr_n': "This is my description",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description"
    assert spell.AtHigherLevels == ""
    assert spell.Ritual == True


def test_from_engl393_ritual_end():
    test_info = {
        'level_and_type': "1st-level divination (Ritual)",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S",
        'duration': "30 minutes",
        'descr_n': "This is my description",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description"
    assert spell.AtHigherLevels == ""
    assert spell.Ritual == True


def test_from_engl393_space_in_level():
    test_info = {
        'level_and_type': "1 st-level divination",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S",
        'duration': "30 minutes",
        'descr_n': "This is my description",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description"
    assert spell.AtHigherLevels == ""
    assert spell.Ritual == False


def test_from_engl393_at_higher_levels():
    test_info = {
        'level_and_type': "1st-level divination",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S",
        'duration': "30 minutes",
        'descr_n': "This is my description. At Higher Levels: cool stuff happens",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description."
    assert spell.AtHigherLevels == "cool stuff happens"
    assert spell.Ritual == False


def test_from_engl393_at_higher_levels_dot():
    test_info = {
        'level_and_type': "1st-level divination",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S",
        'duration': "30 minutes",
        'descr_n': "This is my description. At Higher Levels. cool stuff happens",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description."
    assert spell.AtHigherLevels == "cool stuff happens"
    assert spell.Ritual == False


def test_from_engl393_material_no_components():
    test_info = {
        'level_and_type': "1st-level divination",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S, M",
        'duration': "30 minutes",
        'descr_n': "This is my description",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description"
    assert spell.AtHigherLevels == ""
    assert spell.Ritual == False


def test_from_engl393_material_components():
    test_info = {
        'level_and_type': "1st-level divination",
        'cast_time': "1 action",
        'range': "10 feet",
        'components': "V, S, M (an expensive thing)",
        'duration': "30 minutes",
        'descr_n': "This is my description",
    }
    spell = Spell.from_engl393("testName", test_info)
    assert spell.Level == 1
    assert spell.School == "Divination"
    assert spell.CastTime == "1 action"
    assert spell.Range == "10 feet"
    assert spell.Components == ['V', 'S', 'M (an expensive thing)']
    assert spell.Duration == "30 minutes"
    assert spell.Description == "This is my description"
    assert spell.AtHigherLevels == ""
    assert spell.Ritual == False

