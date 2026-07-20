import streamlit as st

# 웹 페이지 제목 및 설명
st.title("🚀 우주 방사선(GCR) 대응 해밍코드 ECC 시뮬레이터")
st.markdown("《코스모스》 탐구활동 - 은하 우주선으로 인한 반도체 비트 반전 오류 정정")

# 1. 데이터 입력 (4비트 이진수)
data_input = st.text_input("원본 데이터 4비트를 입력하세요 (예: 1101):", value="1101", max_chars=4)

if len(data_input) != 4 or not all(c in '01' for c in data_input):
    st.error("⚠️ 0과 1로 이루어진 4비트 데이터를 입력해주세요.")
else:
    d = [int(c) for c in data_input]
    
    # 2. 해밍 코드 인코딩 (7비트 만들기)
    # 패리티 비트 위치: 1, 2, 4 / 데이터 비트 위치: 3, 5, 6, 7
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    
    encoded = [p1, p2, d[0], p3, d[1], d[2], d[3]]
    
    st.subheader("1️⃣ 인코딩 결과 (송신 데이터)")
    st.write(f"패리티 비트가 추가된 7비트 데이터: `{encoded}`")
    
    # 3. 우주 방사선(GCR) 피격 시뮬레이션
    st.subheader("2️⃣ 은하 우주선(GCR) 충격 시뮬레이션")
    error_idx = st.slider("방사선이 타격할 비트 위치를 고르세요 (1~7)", 1, 7, 5)
    
    # GCR 공격으로 비트 반전 (0->1, 1->0)
    corrupted = list(encoded)
    corrupted[error_idx - 1] = 1 - corrupted[error_idx - 1]
    
    st.warning(f"💥 우주 방사선 피격! {error_idx}번 비트가 반전되었습니다.")
    st.write(f"오류가 발생한 데이터: `{corrupted}`")
    
    # 4. 에러 검출 및 복원 (디코딩)
    st.subheader("3️⃣ ECC 알고리즘 작동 (오류 검출 및 복원)")
    
    # 수신된 데이터로 패리티 재계산 (XOR 연산)
    c1 = corrupted[0] ^ corrupted[2] ^ corrupted[4] ^ corrupted[6]
    c2 = corrupted[1] ^ corrupted[2] ^ corrupted[5] ^ corrupted[6]
    c3 = corrupted[3] ^ corrupted[4] ^ corrupted[5] ^ corrupted[6]
    
    # 신도롬(오류 위치) 계산 (이진수 -> 10진수 변환)
    detected_idx = c1 + (c2 * 2) + (c3 * 4)
    
    if detected_idx == 0:
        st.success("✅ 오류가 검출되지 않았습니다. 데이터가 안전합니다.")
    else:
        st.error(f"🔍 오류 감지! 수학적 연산 결과 [ {detected_idx}번 비트 ]에 에러가 존재합니다.")
        
        # 오류 비트 복원
        fixed = list(corrupted)
        fixed[detected_idx - 1] = 1 - fixed[detected_idx - 1]
        
        # 원본 데이터 추출
        restored_data = f"{fixed[2]}{fixed[4]}{fixed[5]}{fixed[6]}"
        
        st.success(f"🛠️ 자동으로 복원된 7비트 데이터: `{fixed}`")
        st.info(f"✨ 최종 복구된 원본 데이터: **{restored_data}** (입력값 데이터와 일치!)")
