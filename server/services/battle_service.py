import random
from models.general_model import GeneralModel
from models.skill_model import SkillModel

general_model = GeneralModel()
skill_model = SkillModel()

PRIORITY_PREPARE = ['兵种', '阵法', '被动', '指挥']
PRIORITY_BATTLE = PRIORITY_PREPARE + ['主动', '突击', '普通攻击']

def _skill_detail(skill_id):
    if not skill_id:
        return None
    return skill_model.get_skill_by_id(skill_id)

def _attr_for_effect(general, skill):
    effect_types = skill.get('effectTypes', []) if skill else []
    if '谋略' in effect_types:
        return general.get('intelligence', 50)
    return general.get('power', 50)

def _trigger_rate(skill):
    factors = skill.get('impactFactors') if skill else None
    if isinstance(factors, list) and len(factors) > 0:
        rate = factors[0].get('triggerRate', 0)
        coeffs = factors[0].get('coefficients', [])
        coeff = coeffs[0] if coeffs else 10
        return rate, coeff
    return 0, 10

def _resolve_order(generals):
    return sorted(range(len(generals)), key=lambda i: generals[i].get('speed', 50), reverse=True)

def simulate_battle(payload):
    team1 = payload.get('team1', {})
    team2 = payload.get('team2', {})
    g1 = team1.get('generals', [])
    g2 = team2.get('generals', [])
    chief1 = team1.get('chiefIndex', 0)
    chief2 = team2.get('chiefIndex', 2)

    troops1 = [10000, 10000, 10000]
    troops2 = [10000, 10000, 10000]
    log = []

    def apply_skill(att_side, def_side, att_idx, def_idx, skill, phase, round_no):
        rate, coeff = _trigger_rate(skill)
        triggered = random.randint(1, 100) <= rate
        dmg = 0
        if phase == '普通攻击':
            base = (att_side[att_idx].get('power', 50))
            dmg = int(base * 10)
            triggered = True
        else:
            if triggered:
                base = _attr_for_effect(att_side[att_idx], skill)
                dmg = int(base * coeff)
        if triggered and dmg > 0:
            if def_side is g2:
                troops2[def_idx] = max(0, troops2[def_idx] - dmg)
            else:
                troops1[def_idx] = max(0, troops1[def_idx] - dmg)
        log.append({
            'round': round_no,
            'phase': phase,
            'attacker': att_side[att_idx].get('name'),
            'defender': def_side[def_idx].get('name'),
            'skillId': (skill or {}).get('cfgId'),
            'triggered': triggered,
            'damage': dmg,
            'troops1': troops1[:],
            'troops2': troops2[:]
        })

    def is_ended():
        return troops1[chief1] == 0 or troops2[chief2] == 0

    def defend_target(side_troops):
        for i in range(3):
            if side_troops[i] > 0:
                return i
        return 0

    # 准备回合
    order1 = _resolve_order(g1)
    order2 = _resolve_order(g2)
    for phase in PRIORITY_PREPARE:
        for idx in order1:
            if troops1[idx] <= 0 or not g1[idx].get('innateSkillId'):
                continue
            s = _skill_detail(g1[idx].get('innateSkillId'))
            if s and s.get('triggerType') == phase:
                apply_skill(g1, g2, idx, defend_target(troops2), s, phase, 0)
                if is_ended():
                    break
        for idx in order2:
            if troops2[idx] <= 0 or not g2[idx].get('innateSkillId'):
                continue
            s = _skill_detail(g2[idx].get('innateSkillId'))
            if s and s.get('triggerType') == phase:
                apply_skill(g2, g1, idx, defend_target(troops1), s, phase, 0)
                if is_ended():
                    break
        if is_ended():
            break

    # 战斗回合 1..8
    for r in range(1, 9):
        for phase in PRIORITY_BATTLE:
            # 队伍1出手
            for idx in order1:
                if troops1[idx] <= 0:
                    continue
                # 自带战法
                innate_id = g1[idx].get('innateSkillId')
                if innate_id:
                    s = _skill_detail(innate_id)
                    if s and s.get('triggerType') == phase:
                        apply_skill(g1, g2, idx, defend_target(troops2), s, phase, r)
                        if is_ended():
                            break
                # 其他战法（第二、第三格）
                extra_skills = g1[idx].get('skills', [None, None, None])
                for pos in [1, 2]:
                    sid = None
                    if isinstance(extra_skills, list) and len(extra_skills) > pos:
                        item = extra_skills[pos]
                        sid = item.get('cfgId') if isinstance(item, dict) else item
                    if sid:
                        s = _skill_detail(sid)
                        if s and s.get('triggerType') == phase:
                            apply_skill(g1, g2, idx, defend_target(troops2), s, phase, r)
                            if is_ended():
                                break
                if phase == '普通攻击' and not is_ended():
                    apply_skill(g1, g2, idx, defend_target(troops2), None, phase, r)
                if is_ended():
                    break

            # 队伍2出手
            for idx in order2:
                if troops2[idx] <= 0:
                    continue
                innate_id = g2[idx].get('innateSkillId')
                if innate_id:
                    s = _skill_detail(innate_id)
                    if s and s.get('triggerType') == phase:
                        apply_skill(g2, g1, idx, defend_target(troops1), s, phase, r)
                        if is_ended():
                            break
                extra_skills = g2[idx].get('skills', [None, None, None])
                for pos in [1, 2]:
                    sid = None
                    if isinstance(extra_skills, list) and len(extra_skills) > pos:
                        item = extra_skills[pos]
                        sid = item.get('cfgId') if isinstance(item, dict) else item
                    if sid:
                        s = _skill_detail(sid)
                        if s and s.get('triggerType') == phase:
                            apply_skill(g2, g1, idx, defend_target(troops1), s, phase, r)
                            if is_ended():
                                break
                if phase == '普通攻击' and not is_ended():
                    apply_skill(g2, g1, idx, defend_target(troops1), None, phase, r)
                if is_ended():
                    break

            if is_ended():
                break
        if is_ended():
            break

    winner = None
    if troops1[chief1] == 0 and troops2[chief2] == 0:
        winner = 'draw'
    elif troops1[chief1] == 0:
        winner = 'team2'
    elif troops2[chief2] == 0:
        winner = 'team1'
    else:
        # 未分出胜负，比较主将剩余兵力
        winner = 'team1' if troops1[chief1] >= troops2[chief2] else 'team2'

    return {
        'winner': winner,
        'finalTroops': {
            'team1': troops1,
            'team2': troops2
        },
        'rounds': len([e for e in log if e.get('phase') == '普通攻击' or e.get('skillId')]),
        'log': log
    }

