---
title: codex + twilio 起床尿尿
date: 2026-05-13 15:42:18
tags:
---
&nbsp;
<!-- more -->

筆記下起床尿尿的功能, 以後有重要事件就不怕沒人打 morning call

dot env
```
TWILIO_ACCOUNT_SID=AC8a8955984xxxxxxxxx
TWILIO_AUTH_TOKEN=05xxxxxxxxx
TWILIO_PHONE_NUMBER=+151232324342
MORNING_CALL_TO=+886987654321
MORNING_CALL_MESSAGE=起床尿尿了。
```

主程式
```py
import os
import sys

from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


def require_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"缺少環境變數：{name}", file=sys.stderr)
        sys.exit(1)
    return value


def build_twiml(message):
    return f"""
<Response>
    <Say language="zh-TW">
        {message}
    </Say>
    <Pause length="1"/>
    <Say language="zh-TW">
        再提醒一次，該起床尿尿了。
    </Say>
</Response>
""".strip()


def main():
    load_dotenv()

    account_sid = require_env("TWILIO_ACCOUNT_SID")
    auth_token = require_env("TWILIO_AUTH_TOKEN")
    from_number = require_env("TWILIO_PHONE_NUMBER")
    to_number = require_env("MORNING_CALL_TO")

    message = os.environ.get("MORNING_CALL_MESSAGE", "早安，該起床了。")

    client = Client(account_sid, auth_token)

    try:
        call = client.calls.create(
            twiml=build_twiml(message),
            to=to_number,
            from_=from_number,
        )
    except TwilioRestException as exc:
        print("撥打失敗。Twilio 回傳錯誤：", file=sys.stderr)
        print(f"狀態碼：{exc.status}", file=sys.stderr)
        print(f"錯誤代碼：{exc.code}", file=sys.stderr)
        print(f"訊息：{exc.msg}", file=sys.stderr)
        sys.exit(1)

    print("已送出撥打請求")
    print(f"Call SID: {call.sid}")


if __name__ == "__main__":
    main()

```
