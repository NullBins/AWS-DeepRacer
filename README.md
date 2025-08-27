<div align="center">
  <h1>< ⭐AWS-DeepRacer🚘 ></h1>
  - AWS DeepRacer reinforcement learning model creation training -
</div>

## 우리 팀의 목표 (Our team's goal)
- 예선 통과 ( 제발!! )

## AWS DeepRacer란?
### AWS DeepRacer는 강화 학습으로 구동되는 완전 자율 주행 (1/18 비율의) 경주용 자동차임.
- AWS DeepRacer 콘솔: 3차원 시뮬레이션 자율 주행 환경에서 강화 학습 모델을 훈련 및 평가하기 위한 AWS 기계 학습 서비스
  * 콘솔을 사용하면 강화 학습 모델을 훈련하거나, AWS DeepRacer 시뮬레이터에서 모델 성능을 평가할 수 있다.
- AWS DeepRacer 차량: 자율 주행을 목적으로 훈련된 AWS DeepRacer 모델에 대해 추론을 실행할 수 있는 1/18 비율의 RC 자동차
  * AWS DeepRacer 차량은 Wi-Fi가 지원되는 물리적 차량으로서 물리적 트랙에서 강화 학습 모델을 사용해 스스로 주행할 수 있다.
 
## 강화 학습(Reinforcement Learning)
### AWS DeepRacer에서 강화 학습의 목적은 임의 환경에서 최적의 정책📑을 학습👨‍🏫하는 데 있다. (핵심)
- 여기에서 학습이란 시행 착오가 반복🔄되는 프로세스를 말한다.
- 에이전트는 무작위로 초기 행동을 보이면서 새로운 상태에 도달한다.
- 그런 다음 해당 단계를 반복하여 새로운 상태에서 다음 상태로 넘어간다.
- 에이전트는 시간이 지나면서 이러한 방식으로 장기적 보상🎁을 극대화하는 행동을 발견한다.
- 초기 상태에서 최종 상태까지 이어지는 에이전트의 상호 작용을 에피소드(Episode)라고 부른다.
### 다음은 학습 프로세스를 나타낸다.
- [ Agent ] -> action a(Subscript t) -> [ Environment ] -> state s(t+1), reward r(t+1) -> [ Agent ]
- 에이전트는 신경망을 구체화하고, 신경망은 에이전트의 정책에 대한 근사 함수를 표현한다.
- 차량의 정방 카메라에서 촬영된 이미지는 환경 상태이고, 에이전트 행동은 에이전트의 **속도**와 **조향 각도**로 결정된다.
- *에이전트가 트랙을 벗어나지 않고 완주하면 양의 보상을, 그리고 트랙에서 벗어나면 음의 보상을 받는다.*
- 그리고 **에피소드는 레이스 트랙의 임의 구간에서 에이전트와 함께 시작되어 에이전트가 트랙에서 벗어나거나 한 바퀴를 완주할 때 종료된다.**

## 행동 공간 및 보상 함수
- 강화 학습에서는 에이전트가 환경과 상호 작용할 때 사용할 수 있는 모든 유효한 행동 또는 선택의 집합을 **행동 공간**이라고 한다.
- AWS DeepRacer 차량은 *회전이 가까워지면 가속 또는 제동* 후 **좌회전**, **우회전** 또는 **직진** 중 하나를 선택할 수 있다.
- 이러한 동작은 조향 각도와 속도의 조합으로 정의되어 에이전트를 위한 옵션 메뉴(0~9)를 생성한다.
- 예를 들어 0은 -30도 및 0.4m/s, 1은 -30도 및 0.8m/s, 2는 -15도 및 0.4m/s, 3은 -15도 및 0.8m/s, 3은 -15도 및 0.8m/s 등 9까지 나타낼 수 있다.
- 각도가 *음수*이면 차를 **오른쪽**으로 돌리고, *양수*이면 차를 **왼쪽**으로 돌리고, 0이면 바퀴가 똑바로 유지된다.
### 보상 함수(Reward Function)
- 에이전트는 환경을 탐색하면서 가치 함수를 학습한다.
- 가치 함수는 에이전트가 환경을 관찰한 후 취한 행동이 얼마나 좋은지 판단하는 데 도움이 된다.
- 가치 함수는 AWS DeepRacer 콘솔에서 작성한 보상 함수를 사용하여 행동에 점수를 매긴다.
- 예를 들어, AWS DeepRacer 콘솔의 센터 라인 따르기 샘플 보상 기능에서 좋은 행동은 에이전트를 트랙 중앙에 가깝게 유지하고 에이전트를 트랙 중앙에서 멀어지게 하는 잘못된 행동보다 높은 점수를 받게 하는 것이다.

## 우리팀이 사용한 보상함수(RF)
```python
import math

""" 트랙의 진행 방향과 차량의 현재 헤딩(heading)이
    얼마나 일치하는지를 평가하는 보상 함수 """

# (params)에 스텝마다 넘겨주는 상태 정보들이 딕셔너리 형태로 담겨 있음
def reward_function(params):  
    waypoints = params['waypoints'] # 트랙 위의 고정된 좌표 리스트 예) [(1,2),(3,4), ... ]
    closest_waypoints = params['closest_waypoints'] # 차량에 가장 가까운 두 개의 waypoint 인덱스 값 [앞, 뒤]
    heading = params['heading'] # 차량이 현재 바라보고 있는 방향(degree)

    reward = 1.0

    # 차량의 진행 방향을 계산하기 위한, 현재 위치 기준의
    # 이전 waypoint와 다음 waypoint를 선언
    next_point = waypoints[closest_waypoints[1]] # 다음 waypoint
    prev_point = waypoints[closest_waypoints[0]] # 이전 waypoint

    # 차량이 따라가야 할 진행 방향을 구하기 위한 기준
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Arctan(waypoint y의 차이, waypoint x의 차이) [각도의 라디안 단위]
    track_direction = math.degrees(track_direction) # 라디안을 각도(degree)로 바꿈
    direction_diff = abs(track_direction - heading) # 실제 차량이 바라보고 있는 값의 차이를 구함
    if direction_diff > 180: # 180도 이상이면 반대 방향으로 도는게 효율적
        direction_diff = 360 - direction_diff # 각도는 원형이기에 (360 - 차이)로 계산
    DIRECTION_THRESHOLD = 10.0 # 방향의 임계값(기준각도)
    if direction_diff > DIRECTION_THRESHOLD: # 10도 이상 차이나면
        reward *= max(0.0, 1.0 - (direction_diff / 50)) # 각도 차이에 따라 보상값을 유연하게 깎아버림

    return float(reward)
```

## 대회 결과 [ 경기대 제3회 AWS DeepRacer 경진대회 ]
### 우승! 🏆 (Team: Z1존끝판종결ZA)
> [![Video](http://img.youtube.com/vi/YPxOdy3E4a0/0.jpg)](https://www.youtube.com/watch?v=YPxOdy3E4a0)
