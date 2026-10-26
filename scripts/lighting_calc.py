#!/usr/bin/env python3
"""户外照明参数计算工具：流明法估灯数、太阳能系统配比、杆高间距经验值。"""
import argparse
import sys


def cmd_lumen(args):
    """流明法: N = (E*A) / (F*CU*MF)"""
    needed_lumens = args.area * args.target_lux
    effective = args.fixture_lumen * args.cu * args.mf
    if effective <= 0:
        sys.exit("错误: 单灯光通量/利用系数/维护系数必须大于 0")
    n = needed_lumens / effective
    import math
    n_up = math.ceil(n)
    print(f"照明面积        : {args.area} m²")
    print(f"目标维持照度    : {args.target_lux} lx")
    print(f"所需总光通量    : {needed_lumens:.0f} lm")
    print(f"单灯有效光通量  : {effective:.0f} lm (CU={args.cu}, MF={args.mf})")
    print(f"理论灯数        : {n:.2f}")
    print(f"建议安装数量    : {n_up} 套")
    actual = effective * n_up / args.area
    print(f"安装后预估照度  : {actual:.1f} lx")


def cmd_solar(args):
    """太阳能配比: 日耗电 → 电池 → 光伏板"""
    daily_wh = args.load_w * args.hours
    battery_wh = daily_wh * args.rain_days / args.dod
    pv_w = daily_wh * (args.rain_days + 1) / (args.sun_hours * 0.75)
    pv_w_rec = pv_w * 1.15
    print(f"LED 负载        : {args.load_w} W × {args.hours} h/晚")
    print(f"日耗电量        : {daily_wh:.0f} Wh")
    print(f"连续阴雨天      : {args.rain_days} 天 (DOD={args.dod})")
    print(f"电池容量需求    : {battery_wh:.0f} Wh")
    if args.voltage:
        print(f"  → {args.voltage}V 系统 ≈ {battery_wh/args.voltage:.1f} Ah")
    print(f"峰值日照时数    : {args.sun_hours} h (系统效率按 75%)")
    print(f"光伏板计算功率  : {pv_w:.0f} Wp")
    print(f"建议配置(留15%余量): {pv_w_rec:.0f} Wp")
    print("提示: 若支持感应降功率, 可按平均功率的 60-70% 重新核算以缩小配比。")


def cmd_pole(args):
    """杆高间距经验值"""
    spacing = args.pole_height * 3.2
    arm = args.pole_height * 0.1
    depth = args.pole_height / 7
    ratio = spacing / args.road_width if args.road_width else 0
    print(f"杆高            : {args.pole_height} m")
    print(f"建议间距        : {spacing:.1f} m (杆高×3~3.5)")
    if args.road_width:
        print(f"路宽            : {args.road_width} m")
        print(f"间距/路宽比     : {ratio:.2f}")
        if args.road_width <= args.pole_height * 1.2:
            print("布灯方式        : 单侧布灯可行")
        elif args.road_width <= args.pole_height * 2.2:
            print("布灯方式        : 建议双侧交错布灯")
        else:
            print("布灯方式        : 建议双侧对称布灯或中央布灯")
    print(f"悬挑臂长        : ≈{arm:.1f} m (杆高×0.1)")
    print(f"灯杆埋深        : ≈{depth:.1f} m (杆高×1/6~1/8, 以基础图纸为准)")


def main():
    p = argparse.ArgumentParser(description="户外照明参数计算工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("lumen", help="流明法估算灯具数量")
    pl.add_argument("--area", type=float, required=True, help="照明面积 m²")
    pl.add_argument("--target-lux", type=float, required=True, help="目标维持照度 lx")
    pl.add_argument("--fixture-lumen", type=float, required=True, help="单灯光通量 lm")
    pl.add_argument("--cu", type=float, default=0.7, help="利用系数, 默认0.7")
    pl.add_argument("--mf", type=float, default=0.8, help="维护系数, 默认0.8")
    pl.set_defaults(func=cmd_lumen)

    ps = sub.add_parser("solar", help="太阳能系统配比计算")
    ps.add_argument("--load-w", type=float, required=True, help="LED 功率 W")
    ps.add_argument("--hours", type=float, required=True, help="每晚工作小时数")
    ps.add_argument("--sun-hours", type=float, required=True, help="当地峰值日照时数 h")
    ps.add_argument("--rain-days", type=float, default=3, help="连续阴雨天数, 默认3")
    ps.add_argument("--dod", type=float, default=0.8, help="电池放电深度, 默认0.8")
    ps.add_argument("--voltage", type=float, help="系统电压 V (可选, 用于换算Ah)")
    ps.set_defaults(func=cmd_solar)

    pp = sub.add_parser("pole", help="杆高与间距经验计算")
    pp.add_argument("--pole-height", type=float, required=True, help="灯杆高度 m")
    pp.add_argument("--road-width", type=float, help="道路宽度 m (可选)")
    pp.set_defaults(func=cmd_pole)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
