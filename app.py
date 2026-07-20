import streamlit as st

# 웹 페이지 제목 및 탐구 배경
st.title("🚀 우주 방사선(GCR) 대응 해밍코드(ECC) 시뮬레이터")
st.markdown("### 《코스모스》 탐구활동 - 은하 우주선으로 인한 반도체 비트 반전 오류 정정")
st.markdown("---")

# [이론 설명 섹션] XOR 개념과 패리티 규칙 통합 가이드
st.sidebar.header("📚 핵심 개념 쏙쏙 가이드")
st.sidebar.markdown("""
### 1. XOR(배타적 논리합) 연산이란?
컴퓨터가 에러를 잡을 때 쓰는 가장 중요한 논리 연산입니다. 
* **규칙:** 비교하는 **두 값이 서로 다를 때만 1(True)** 이 나오고, **같으면 0(False)** 이 나옵니다.

| 입력 A | 입력 B | **XOR 결과 (A ^ B)** |
| :---: | :---: | :---: |
| 0 | 0 | **0** (같으니까) |
| 0 | 1 | **1** (다르니까) |
| 1 | 0 | **1** (다르니까) |
| 1 | 1 | **0** (같으니까) |

💡 **해밍코드의 특징:** 어떤 숫자들을 싹 다 XOR 연산했을 때 결과가 `0`이 나오면 "에러 없음"을 뜻하고, `1`이 나오면 무언가 변형되었다는 것을 컴퓨터가 빛의 속도로 알아차릴 수 있습니다!

---

### 2. 패리티 비트(Parity Bit)란?
데이터 전송 과정에서 오류가 생겼는지 검사하고 수정하기 위해 **기존 데이터에 추가하는 '체크용 덤 비트'** 입니다.

### 3. 해밍코드의 패리티 규칙
총 7비트 중 **1번, 2번, 4번(2의 거듭제곱 자리)** 을 패리티 비트($P_1, P_2, P_3$)로 비워둡니다.
나머지 3, 5, 6, 7번에 원본 데이터($D_1, D_2, D_3, D_4$)를 넣고 위의 **XOR 연산** 을 통해 비트를 채웁니다.
""")

# 1. 데이터 입력 (4비트 이진수)
st.subheader("💡 1단계: 원본 데이터 입력 및 패리티 규칙 적용")
data_input = st.text_input("원본 데이터 4비트를 입력하세요 (예: 1101):", value="1101", max_chars=4)

if len(data_input) != 4 or not all(c in '01' for c in data_input):
    st.error("⚠️ 0과 1로 이루어진 4비트 데이터를 입력해주세요.")
else:
    d = [int(c) for c in data_input]
    
    # 해밍 코드 인코딩 규칙에 따른 패리티 계산
    # 두 값이 같으면 0, 다르면 1이 나오는 XOR(^) 연산 활용
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    
    encoded = [p1, p2, d[0], p3, d[1], d[2], d[3]]
    
    # 규칙 시각화 설명
    st.markdown(f"""
    **[패리티 비트 생성 완료]**
    * 입력한 데이터: `{d[0]}`, `{d[1]}`, `{d[2]}`, `{d[3]}`
    * 계산된 패리티 비트: $P_1$=`{p1}`, $P_2$=`{p2}`, $P_3$=`{p3}`
    """)
    st.info(f"정해진 규칙(위치)대로 병합된 **7비트 송신 데이터**: `{encoded}`")
    st.markdown("---")
    
    # 2. 우주 방사선(GCR) 피격 시뮬레이션
    st.subheader("💥 2단계: 은하 우주선(GCR) 충격 (비트 반전)")
    st.markdown("대기권 밖 우주 공간에서 방사선이 반도체를 타격하여 **특정 비트의 전하가 뒤바뀌는(반전될) 상황**을 인위적으로 만들어봅니다.")
    
    error_idx = st.slider("방사선이 타격할(반전시킬) 비트 위치를 고르세요 (1~7번)", 1, 7, 5)
    
    # GCR 공격으로 비트 반전 (0->1, 1->0)
    corrupted = list(encoded)
    corrupted[error_idx - 1] = 1 - corrupted[error_idx - 1]
    
    st.warning(f"🚨 우주 방사선 피격! 현재 **{error_idx}번 비트**가 전하 충격으로 반전되었습니다.")
    st.write(f"오류가 발생한(변형된) 데이터 상태: `{corrupted}`")
    st.markdown("---")
    
    # 3. 에러 검출 및 복원 (디코딩)
    st.subheader("🔍 3단계: ECC 알고리즘 작동 (수학적 오류 복원)")
    st.markdown("수신 장치는 들어온 7비트 데이터를 다시 규칙대로 XOR 연산(신도롬 계산)하여 깨진 자리를 찾아냅니다.")
    
    # 수신된 데이터로 패리티 재계산 (신도롬 체크)
    c1 = corrupted[0] ^ corrupted[2] ^ corrupted[4] ^ corrupted[6]
    c2 = corrupted[1] ^ corrupted[2] ^ corrupted[5] ^ corrupted[6]
    c3 = corrupted[3] ^ corrupted[4] ^ corrupted[5] ^ corrupted[6]
    
    # 이진수 조합을 통해 10진수 오류 인덱스 도출
    detected_idx = c1 + (c2 * 2) + (c3 * 4)
    
    st.markdown(f"""
    **[수신측 XOR 계산 결과 (신도롬)]**
    * $C_1$ = `{c1}`, $C_2$ = `{c2}`, $C_3$ = `{c3}` 
    * 이진수 코드를 10진수로 변환한 값: **{detected_idx}**
    """)
    
    if detected_idx == 0:
        st.success("✅ 오류가 검출되지 않았습니다. 데이터가 아주 안전합니다.")
    else:
        st.error(f"🎯 오류 검출 성공! 수학적 계산 결과 **[ {detected_idx}번 비트 ]**가 반전되었음을 알아냈습니다.")
        
        # 오류 비트 다시 뒤집어서 복원 (1->0, 0->1)
        fixed = list(corrupted)
        fixed[detected_idx - 1] = 1 - fixed[detected_idx - 1]
        
        # 원본 4비트만 다시 추출
        restored_data = f"{fixed[2]}{fixed[4]}{fixed[5]}{fixed[6]}"
        
        st.success(f"🛠️ **자동 복원된 7비트 데이터**: `{fixed}`")
        st.success(f"✨ **최종 복구된 원본 데이터**:  **{restored_data}** (처음 입력한 값과 완벽히 일치!)")
