#!/usr/bin/env python3
"""
ARGOS-Roach model generator.
Generates models/hexapod.xml for MuJoCo (headless, physics only).

UNITS: meters (m), kilograms (kg), radians (rad), seconds (s). Forces: N, torques: N*m.

DESIGN (realistic ~30 cm span hexapod, NOT a 1:1 scaled cockroach):
  - Body: box 0.16 x 0.12 x 0.035 m, mass 0.70 kg (printed chassis + battery).
  - 6 legs x 3 joints = 18 position actuators:
      coxa  (yaw at body,   axis = body Z)   range [-0.8, 0.8] rad
      femur (lift,          axis = local X)  range [-1.3, 1.3] rad
      tibia (knee bend,     axis = local X)  range [-2.6, 2.6] rad
  - Segments: coxa box 0.05 m (0.035 kg); femur capsule 0.08 m (0.055 kg);
    tibia capsule 0.08 m (0.045 kg); foot sphere r=0.016 m (0.005 kg).
    Total mass ~1.54 kg.
  - Actuators: position servos, kp = 60 (N*m/rad), gear 1, force limit
    +-2.5 N*m (mid-size servo, e.g. AX-12 class ~1.5 N*m stall, derated).
  - Joint damping: coxa 0.5, femur/tibia 0.8 (N*m*s/rad); frictionloss 0.02 N*m.
  - Standing pose q0 (rad): coxa 0.0, femur s*0.8, tibia -s*1.45 (s = side sign).
  - Leg numbering (tripod gait): 0 RF, 1 LF, 2 LM, 3 RM, 4 RR, 5 LR.
    Tripod A = {0,2,4}, Tripod B = {1,3,5} (diagonal tripods, antiphase).
  - Hips at x in {+0.07, 0, -0.07}, y = +-0.065, z = -0.02 (body frame).
"""

import os

# ---------------- parameters (single source of truth) ----------------
BODY_LEN, BODY_WID, BODY_H = 0.16, 0.12, 0.035
BODY_MASS = 0.70
HIP_X = [0.07, 0.07, 0.0, 0.0, -0.07, -0.07]     # legs 0..5
HIP_Y_SIGN = [1, -1, -1, 1, 1, -1]                # side sign per leg
HIP_Z = -0.02
COXA_LEN = 0.05
FEMUR_LEN, FEMUR_R = 0.08, 0.012
TIBIA_LEN, TIBIA_R = 0.08, 0.010
FOOT_R = 0.016
M_COXA, M_FEMUR, M_TIBIA, M_FOOT = 0.035, 0.055, 0.045, 0.005
JOINT_RANGE = {
    "coxa": (-0.8, 0.8),
    "femur": (-1.3, 1.3),
    "tibia": (-2.6, 2.6),
}
Q0 = {"coxa": 0.0, "femur": 0.8, "tibia": 1.45}   # femur: s*0.8, tibia: -s*1.45
KP = 60.0
FORCE_LIMIT = 2.5                                # N*m
CTRL_RANGE = (-1.5, 1.5)
DAMP = {"coxa": 0.5, "femur": 0.8, "tibia": 0.8}
ARMATURE = {"coxa": 0.0, "femur": 0.01, "tibia": 0.01}
FRICTIONLOSS = 0.02
BODY_START_Z = 0.15
TIMESTEP = 0.002

def side(leg):
    return HIP_Y_SIGN[leg]

def leg_xml(leg):
    s = side(leg)
    hx, hy = HIP_X[leg], s * 0.065
    coxa_box = (0.011, COXA_LEN / 2, 0.011)      # half extents
    return f"""
    <body name="coxa{leg}" pos="{hx} {hy} {HIP_Z}">
      <joint name="j_coxa{leg}" type="hinge" axis="0 0 1"
             range="{JOINT_RANGE['coxa'][0]} {JOINT_RANGE['coxa'][1]}"
             damping="{DAMP['coxa']}" frictionloss="{FRICTIONLOSS}"/>
      <geom name="coxa{leg}" type="box" size="{coxa_box[0]} {coxa_box[1]} {coxa_box[2]}"
            pos="0 {s*COXA_LEN/2} 0" mass="{M_COXA}" rgba="0.55 0.42 0.30 1"/>
      <body name="femur{leg}" pos="0 {s*COXA_LEN} 0">
        <joint name="j_femur{leg}" type="hinge" axis="1 0 0"
               range="{JOINT_RANGE['femur'][0]} {JOINT_RANGE['femur'][1]}"
               damping="{DAMP['femur']}" armature="{ARMATURE['femur']}" frictionloss="{FRICTIONLOSS}"/>
        <geom name="femur{leg}" type="capsule" size="{FEMUR_R} {FEMUR_LEN/2}"
              pos="0 0 -{FEMUR_LEN/2}" mass="{M_FEMUR}" rgba="0.45 0.38 0.30 1"/>
        <body name="tibia{leg}" pos="0 0 -{FEMUR_LEN}">
          <joint name="j_tibia{leg}" type="hinge" axis="1 0 0"
                 range="{JOINT_RANGE['tibia'][0]} {JOINT_RANGE['tibia'][1]}"
                 damping="{DAMP['tibia']}" armature="{ARMATURE['tibia']}" frictionloss="{FRICTIONLOSS}"/>
          <geom name="tibia{leg}" type="capsule" size="{TIBIA_R} {TIBIA_LEN/2}"
                pos="0 0 -{TIBIA_LEN/2}" mass="{M_TIBIA}" rgba="0.38 0.33 0.27 1"/>
          <geom name="foot{leg}" type="sphere" size="{FOOT_R}" pos="0 0 -{TIBIA_LEN*0.94}"
                mass="{M_FOOT}" rgba="0.2 0.2 0.2 1" condim="3" priority="1"/>
        </body>
      </body>
    </body>"""

def actuator_xml():
    out = []
    for leg in range(6):
        for j in ("coxa", "femur", "tibia"):
            out.append(f'    <position name="a_{j}{leg}" joint="j_{j}{leg}" kp="{KP}" '
                       f'ctrlrange="{CTRL_RANGE[0]} {CTRL_RANGE[1]}" '
                       f'forcerange="-{FORCE_LIMIT} {FORCE_LIMIT}" gear="1"/>')
    return "\n".join(out)

def excludes_xml():
    return "\n".join(f'    <exclude body1="coxa{leg}" body2="tibia{leg}"/>' for leg in range(6))

def build():
    legs = "\n".join(leg_xml(i) for i in range(6))
    params_note = f"""
<!-- ================= ARGOS-Roach model parameters (UNITS: m, kg, rad, s) =================
  body      : box {BODY_LEN} x {BODY_WID} x {BODY_H} m, mass {BODY_MASS} kg
  coxa      : box length {COXA_LEN} m, mass {M_COXA} kg, yaw joint range {JOINT_RANGE['coxa']} rad
  femur     : capsule length {FEMUR_LEN} m, r {FEMUR_R} m, mass {M_FEMUR} kg, range {JOINT_RANGE['femur']} rad
  tibia     : capsule length {TIBIA_LEN} m, r {TIBIA_R} m, mass {M_TIBIA} kg, range {JOINT_RANGE['tibia']} rad
  foot      : sphere r {FOOT_R} m, mass {M_FOOT} kg
  total mass: {BODY_MASS + 6*(M_COXA+M_FEMUR+M_TIBIA+M_FOOT)} kg ; leg span ~0.28 m tip-to-tip
  actuators : 18 position servos, kp {KP} N*m/rad, gear 1, |force| <= {FORCE_LIMIT} N*m
  standing q0 (rad): coxa 0, femur s*{Q0['femur']}, tibia -s*{Q0['tibia']}  (s=+1 right, -1 left)
  timestep {TIMESTEP} s, Euler integrator, pyramidal friction cone.
  Body moves ONLY via foot-floor contact (free joint, no external forces).
============================================================================================ -->
"""
    return f"""<mujoco model="argos_roach">
{params_note}
  <compiler angle="radian" autolimits="true"/>
  <option timestep="{TIMESTEP}" integrator="Euler" cone="pyramidal" iterations="50"
          solver="Newton" jacobian="dense"/>

  <worldbody>
    <geom name="floor" type="plane" size="10 10 0.1" pos="0 0 0"
          friction="0.8 0.005 0.0001" condim="3" rgba="0.7 0.7 0.7 1"/>
    <body name="body" pos="0 0 {BODY_START_Z}">
      <freejoint/>
      <geom name="body_geom" type="box" size="{BODY_LEN/2} {BODY_WID/2} {BODY_H/2}"
            mass="{BODY_MASS}" rgba="0.25 0.35 0.55 1"/>
{legs}
    </body>
  </worldbody>

  <contact>
{excludes_xml()}
  </contact>

  <actuator>
{actuator_xml()}
  </actuator>
</mujoco>
"""

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hexapod.xml")
    with open(out, "w") as f:
        f.write(build())
    print(f"wrote {out}")
