#!/usr/bin/env python3
"""
RaptorX Research Challenge — Live Production Verification Script
================================================================
Queries https://www.raptorx.trade/api/reports/<reportId> directly on RaptorX's
production backend (authenticated with x-user-id: cmvtatm8c0001kz075dqtzks5)
to verify all 5 Solana intelligence reports and all 30 persisted REX AI 5.0
multi-turn interrogation messages (15 user questions + 15 assistant responses).
"""

import json
import subprocess
import sys

USER_ID = "cmvtatm8c0001kz075dqtzks5"
WALLET = "Dpd5z1quMeBwPBkKCQNHnjdU6taSLAAcetpon83vgQVe"
USERNAME = "Tiger1055"

REPORTS = [
    {
        "symbol": "CARDS",
        "name": "Collector Crypt",
        "chain": "solana",
        "contractAddress": "CARDSccUMFKoPRZxt5vt3ksUbxEFEcnZ3H2pd3dKxYjp",
        "reportId": "cmvtauoqi0003kt08qspd2wnj",
        "conversationId": "cmvtauoqj0004kt08csxw5x54",
    },
    {
        "symbol": "JUP",
        "name": "Jupiter",
        "chain": "solana",
        "contractAddress": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
        "reportId": "cmvtaw1ad0008i607fbri8d84",
        "conversationId": "cmvtaw1ae0009i607vgrrw9iv",
    },
    {
        "symbol": "KLED",
        "name": "KLEDAI",
        "chain": "solana",
        "contractAddress": "1zJX5gRnjLgmTpq5sVwkq69mNDQkCemqoasyjaPW6jm",
        "reportId": "cmvtaw2zy000bi607olpzctwj",
        "conversationId": "cmvtaw2zy000ci6072wyytjal",
    },
    {
        "symbol": "STONK",
        "name": "STONK",
        "chain": "solana",
        "contractAddress": "6GmAFSYs4gk3FDao5FzzySQpPZaWsa4rUJHacpMpUNgx",
        "reportId": "cmvtavkv70002i607xhak74kk",
        "conversationId": "cmvtavkv70003i607yd89dy4f",
    },
    {
        "symbol": "RAWR",
        "name": "Jurassic Finance",
        "chain": "solana",
        "contractAddress": "4K1m7gAMDKzrxQn68yuZAd767w57Fw7Ykw69dG3umeta",
        "reportId": "cmvtavmfw0005i607g95732yl",
        "conversationId": "cmvtavmfw0006i607rl0qpruh",
    },
]


def main() -> int:
    print("=" * 78)
    print(f"RaptorX Live Production Audit | User: {USERNAME} ({USER_ID})")
    print(f"Solana Wallet: {WALLET}")
    print("=" * 78)

    total_reports = 0
    total_messages = 0
    total_questions = 0

    for item in REPORTS:
        rid = item["reportId"]
        url = f"https://www.raptorx.trade/api/reports/{rid}"
        out = subprocess.check_output(
            ["curl", "-sL", url, "-H", f"x-user-id: {USER_ID}"]
        ).decode("utf-8", errors="ignore")
        payload = json.loads(out)
        rep = payload.get("report")
        assert rep is not None, f"Missing report object for {rid}"
        assert rep.get("id") == rid, f"Mismatched report ID: {rep.get('id')} != {rid}"
        content = rep.get("content", "")
        assert len(content) > 10000, f"Report content too short for {rid}: {len(content)}"

        conv = rep.get("conversation", {})
        msgs = conv.get("messages", [])
        user_msgs = [m for m in msgs if m.get("role") == "user"]
        assistant_msgs = [m for m in msgs if m.get("role") == "assistant"]

        assert len(user_msgs) >= 3, f"Expected >= 3 user questions for {rid}, got {len(user_msgs)}"
        assert len(assistant_msgs) >= 3, f"Expected >= 3 assistant replies for {rid}, got {len(assistant_msgs)}"

        total_reports += 1
        total_messages += len(msgs)
        total_questions += len(user_msgs)

        print(
            f"[PASS] ${item['symbol']:<5} ({item['name']:<17}) | "
            f"reportId={rid} | report_chars={len(content):>6} | "
            f"Q&A_turns={len(user_msgs)} ({len(msgs)} msgs)"
        )
        for idx, q in enumerate(user_msgs, 1):
            q_preview = q.get("content", "").replace("\n", " ")[:95]
            print(f"       Q{idx} [{q.get('id')}]: {q_preview}...")

    print("=" * 78)
    print(
        f"VERIFICATION SUMMARY: PASS 100% | "
        f"{total_reports}/5 Reports Verified | "
        f"{total_questions}/15 Critical Questions Verified | "
        f"{total_messages}/30 Conversation Messages Live on RaptorX DB"
    )
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
