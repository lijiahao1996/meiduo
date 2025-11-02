FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /var/www/html/meiduo_mall
WORKDIR /var/www/html/meiduo_mall

# ✅ 先复制依赖文件
COPY requirements.txt /var/www/html/meiduo_mall/requirements.txt

RUN pip3 install -U "pip<24.1" \
    && pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 install -r requirements.txt \
    && sed -i 's/ungettext/ngettext/g' $(python -c "import site; print(site.getsitepackages()[0])")/haystack/admin.py || true \
    && sed -i 's/ugettext/gettext/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/*.py || true \
    && sed -i 's/ugettext_lazy/gettext_lazy/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/*.py || true

RUN sed -i 's/smart_text/smart_str/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/authentication.py || true \
    && sed -i 's/ugettext/gettext/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/*.py || true \
    && sed -i 's/ugettext_lazy/gettext_lazy/g' $(python -c "import site; print(site.getsitepackages()[0])")/rest_framework_jwt/*.py || true \
    && sed -i 's/ungettext/ngettext/g' $(python -c "import site; print(site.getsitepackages()[0])")/haystack/admin.py || true


# ✅ 修复 django-haystack 兼容性问题 (Django>=4.x 移除了 ungettext)
RUN sed -i 's/ungettext/ngettext/g' $(python -c "import site; print(site.getsitepackages()[0])")/haystack/admin.py || true

# ✅ 拷贝剩余代码
COPY . /var/www/html/meiduo_mall/

RUN chmod +x start.sh && sed -i 's/\r//' start.sh

EXPOSE 8000
CMD ["./start.sh"]

