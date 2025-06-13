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
