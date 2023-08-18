def member(team_name):
    with conn.cursor() as cur:
        # แก้ไข SQL โดยใช้ JOIN เพื่อรวมข้อมูลจาก tb_player, tb_team, และ tb_schools
        cur.execute("""
                        SELECT
                            p.name,
                            p.surname,
                            p.name_player,
                            p.id_gameplayer,
                            s.school_name,
                            COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) AS count_win_2,
                                (
                                SELECT pos.position_name 
                                FROM tb_match
                                INNER JOIN tb_position AS pos ON tb_match.position_id = pos.position_id 
                                WHERE player_id = p.player_id
                                GROUP BY pos.position_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_position_name, 
                            ROUND(AVG(b.kill), 1) AS avg_kill,
                            ROUND(AVG(b.dead), 1) AS avg_dead,
                            ROUND(AVG(b.assist), 1) AS avg_assist,
                            ROUND(AVG((b.kill + b.dead) / b.assist), 1) AS avg_ratio,
                            ROUND(AVG(b.money), 1) AS avg_money,
                            ROUND(AVG(b.point), 1) AS avg_point,
                            ROUND(AVG(b.mvp), 0) AS avg_mvp,
                            ROUND(AVG(b.damage), 1) AS avg_damage,
                            ROUND(AVG(b.damage_), 1) AS avg_damage_,
                            ROUND(AVG(b.take_damage), 1) AS avg_take_damage,
                            ROUND(AVG(b.take_damage_), 1) AS avg_take_damage_,
                            ROUND(AVG(b.teamfight), 1) AS avg_teamfight,
                            ROUND(AVG(b.teamfight_), 1) AS avg_teamfight_,
                            (
                                SELECT h.hero_name
                                FROM tb_match
                                INNER JOIN tb_hero AS h ON tb_match.hero_id = h.hero_id 
                                WHERE player_id = p.player_id
                                GROUP BY h.hero_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_hero_name
                        FROM tb_player AS p
                        INNER JOIN tb_match AS b ON p.player_id = b.player_id
                        INNER JOIN tb_team AS t ON p.team_id = t.team_id
                        INNER JOIN tb_schools AS s ON p.school_id = s.school_id
                        WHERE t.team_name = %s
                        GROUP BY p.name, p.surname, p.name_player, p.id_gameplayer, s.school_name

                    """, (team_name,))
        rows = cur.fetchall()
        logged_in = session.get('logged_in', False)
    return render_template('member.html', data=rows, logged_in=logged_in,team_name=team_name)