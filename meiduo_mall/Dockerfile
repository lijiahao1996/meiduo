FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/html/meiduo_mall

# 先安装依赖
COPY requirements.txt .
RUN pip install -U "pip<24.1" \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt

RUN sed -i 's/ungettext/ngettext/g' $(python -c "import site; print(site.getsitepackages()[0])")/haystack/admin.py || true \
    && sed -i 's/ugettext/gettext/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/*.py || true \
    && sed -i 's/ugettext_lazy/gettext_lazy/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/*.py || true \
    && sed -i 's/smart_text/smart_str/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/authentication.py || true

# 拷贝完整后端代码
COPY . .

RUN chmod +x start.sh && sed -i 's/\r//' start.sh

EXPOSE 8000
CMD ["./start.sh"]

