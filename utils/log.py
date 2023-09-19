import logging

# 로그 기본 설정
logging.basicConfig(
    level=logging.INFO,  # 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='[%(asctime)s-%(levelname)s] %(message)s'
)

LOGGER = logging.getLogger("")

