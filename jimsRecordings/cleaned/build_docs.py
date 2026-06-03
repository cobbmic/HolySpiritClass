#!/usr/bin/env python3
"""Build cleaned Markdown, HTML, and PDF source documents for Jim's Holy Spirit classes."""

from __future__ import annotations

import html
import re
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TXT_DIR = ROOT / "jimsRecordings" / "txt"
OUT_DIR = ROOT / "jimsRecordings" / "cleaned"
CLASS_DIR = OUT_DIR / "classes"
MASTER_MD = OUT_DIR / "holy-spirit-classes.md"
HTML_OUT = OUT_DIR / "holy-spirit-classes.html"
PDF_OUT = OUT_DIR / "holy-spirit-classes.pdf"
CSS_OUT = OUT_DIR / "holy-spirit.css"

TITLE = "The Holy Spirit: Eleven Bible Classes"
SUBTITLE = "Jim Brinkerhoff, Auburn Christian Student Center, Spring 2011"


def bible_link(ref: str) -> str:
    query = ref.replace(" ", "+").replace(":", "%3A").replace("-", "%E2%80%93")
    return f"https://www.biblegateway.com/passage/?search={query}&version=NIV"


CLASSES = [
    {
        "num": 1,
        "file": "hs01.txt",
        "title": "The Forgotten God and the Spirit's Personhood",
        "summary": (
            "Jim opens the series by challenging the habit of ignoring the Holy Spirit. "
            "He begins with the Shema, the Trinity, and the Spirit as a personal divine "
            "being, then introduces the class refrain: the Spirit's work is centered in Jesus Christ."
        ),
        "refs": [
            "Deuteronomy 6:4-5",
            "Genesis 1:2",
            "Genesis 1:26",
            "Matthew 3:16-17",
            "1 Corinthians 12:12-13",
            "John 7:37-39",
            "John 14:16-17",
            "John 14:26",
            "John 15:26-27",
            "John 16:7-15",
            "John 17:20-23",
            "Acts 1:1-8",
            "Acts 2:38-39",
            "Acts 10:39-42",
            "Joel 2:28-32",
        ],
        "quotes": [
            {
                "kind": "author",
                "source": "A. W. Tozer, The Counselor",
                "status": "Verified source for the personhood wording; the transcript paraphrases the quote.",
                "text": (
                    "The Holy Spirit is a person. He is not enthusiasm, courage, energy, "
                    "or a personification of good qualities."
                ),
                "url": "https://sermoncentral.com/sermon-illustrations/2367/in-his-book-the-counselor-a-w-tozer-said-by-alan-stokes",
            },
            {
                "kind": "author",
                "source": "R. A. Torrey, The Person and Work of the Holy Spirit",
                "status": "Verified in the public-domain text; the transcript paraphrases the contrast.",
                "text": (
                    "If the Spirit is treated as a power, the question becomes how to use him; "
                    "if he is a divine person, the question becomes how he will use us."
                ),
                "url": "https://www.gutenberg.org/files/30241/30241-h/30241-h.html",
            },
            {
                "kind": "author",
                "source": "Attributed in the transcript to Francis Schaeffer",
                "status": (
                    "Not verified as Schaeffer. The statement appears in several forms, but I did not find "
                    "a reliable primary citation tying it to Schaeffer."
                ),
                "text": (
                    "How many churches and ministries would carry on as usual if dependence on "
                    "the Holy Spirit and prayer disappeared from the New Testament?"
                ),
                "url": "",
            },
        ],
    },
    {
        "num": 2,
        "file": "hs02.txt",
        "title": "The Spirit of Truth in the Words of Jesus",
        "summary": (
            "The second class works through Jesus' promises in John 14-16. The Spirit is the "
            "Paraclete, teacher, witness, and convicting presence whose ministry points away "
            "from himself and toward Jesus."
        ),
        "refs": [
            "John 14:15-17",
            "John 14:25-26",
            "John 15:26-27",
            "John 16:8-11",
            "John 16:13-15",
            "John 17:6-20",
            "Acts 1:1-3",
            "Acts 2:1-39",
            "Acts 10:39-42",
            "1 Corinthians 1:10-17",
            "Joel 2:28-32",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "John 14:26",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "The Holy Spirit will teach and remind the apostles of what Jesus said.",
                "url": bible_link("John 14:26"),
            },
            {
                "kind": "scripture",
                "source": "John 15:26-27",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "The Spirit testifies about Jesus, and the apostles also testify.",
                "url": bible_link("John 15:26-27"),
            },
        ],
    },
    {
        "num": 3,
        "file": "hs03.txt",
        "title": "Receiving the Spirit: Faith, Jesus, Baptism, and Fullness",
        "summary": (
            "Jim begins the question of how Christians receive the Holy Spirit. He argues from "
            "Romans, Psalm 51, Galatians 3, John 7, Acts 2, and Colossians 2 that the Spirit "
            "is received by grace, in the beginning, through faith centered on Jesus."
        ),
        "refs": [
            "Romans 8:9",
            "Psalm 51:11",
            "1 Samuel 16:13",
            "Galatians 3:1-5",
            "Acts 15",
            "John 7:37-39",
            "Psalm 113-118",
            "Isaiah 12:3",
            "Isaiah 44:3",
            "Acts 2:38-39",
            "Colossians 2:6-15",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "Galatians 3:2-3",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "Did you receive the Spirit by works of law, or by believing what you heard?",
                "url": bible_link("Galatians 3:2-3"),
            },
            {
                "kind": "scripture",
                "source": "John 7:37-39",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "Whoever believes in Jesus receives the living water John identifies with the Spirit.",
                "url": bible_link("John 7:37-39"),
            },
        ],
    },
    {
        "num": 4,
        "file": "hs04.txt",
        "title": "Fullness in Christ and the Washing of Rebirth",
        "summary": (
            "This class completes the receiving-the-Spirit question. Jim connects 1 Corinthians 12, "
            "Colossians 2, Titus 3, and John 3 to present faith, baptism, fullness in Christ, "
            "and the Spirit's renewal in the new birth."
        ),
        "refs": [
            "Romans 8",
            "Psalm 51",
            "Galatians 3",
            "John 7",
            "Acts 2:38-39",
            "1 Corinthians 12:12-13",
            "Colossians 2:8-15",
            "Titus 3:4-7",
            "John 3:3-5",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "1 Corinthians 12:13",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "We were all baptized by one Spirit into one body and given one Spirit to drink.",
                "url": bible_link("1 Corinthians 12:13"),
            },
            {
                "kind": "scripture",
                "source": "Titus 3:4-7",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "God saved us through the washing of rebirth and renewal by the Holy Spirit.",
                "url": bible_link("Titus 3:4-7"),
            },
        ],
    },
    {
        "num": 5,
        "file": "hs05.txt",
        "title": "What Does the Spirit Do? History, Hysteria, and Holiness",
        "summary": (
            "After showing the Toronto Blessing as a case study, Jim traces a theological family "
            "tree from Wesleyan perfectionism through revivalism, the holiness movement, "
            "Pentecostalism, and the charismatic movement. He then turns the question back to "
            "sanctification and the body as the Spirit's temple."
        ),
        "refs": [
            "1 Peter 1:1-2",
            "1 Corinthians 6:18-20",
            "1 Corinthians 12-14",
            "1 Corinthians 15",
            "Romans 8",
            "John 3:3-5",
            "Galatians 5:16-25",
            "Ephesians 4:30",
            "1 Thessalonians 5:19",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "1 Peter 1:1-2",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "Peter names the sanctifying work of the Spirit alongside the Father and Jesus Christ.",
                "url": bible_link("1 Peter 1:1-2"),
            },
            {
                "kind": "scripture",
                "source": "1 Corinthians 6:19-20",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "Your body is the temple of the Holy Spirit; therefore honor God with your body.",
                "url": bible_link("1 Corinthians 6:19-20"),
            },
        ],
    },
    {
        "num": 6,
        "file": "hs06.txt",
        "title": "Sanctification, Scripture, and the Spirit's Power",
        "summary": (
            "Jim develops the Spirit's sanctifying work through Romans 6-8, Philippians 2, "
            "2 Thessalonians 2, and 1 Thessalonians 4. The Spirit does not replace human effort "
            "or Scripture; he works through the word to empower a holy life."
        ),
        "refs": [
            "1 Corinthians 6:18-20",
            "Romans 6",
            "Romans 7",
            "Romans 8:1-14",
            "Philippians 2:12-13",
            "Psalm 119:11",
            "2 Thessalonians 2:13",
            "1 Thessalonians 4:1-8",
            "Galatians 5:22-23",
            "Ephesians 4:30",
            "1 Thessalonians 5:19",
        ],
        "quotes": [
            {
                "kind": "author",
                "source": "Francis Chan, Forgotten God",
                "status": "Verified in widely quoted excerpts and reviews of the book; the transcript paraphrases it.",
                "text": (
                    "If God's Spirit lives in us, there should be a noticeable difference "
                    "between the person who has the Spirit and the person who does not."
                ),
                "url": "https://scottlingle.com/forgotten-god-francis-chan/",
            },
            {
                "kind": "scripture",
                "source": "Romans 8:12-14",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "By the Spirit believers put to death the misdeeds of the body.",
                "url": bible_link("Romans 8:12-14"),
            },
        ],
    },
    {
        "num": 7,
        "file": "hs07.txt",
        "title": "Hope, Intercession, Seal, and Power",
        "summary": (
            "The seventh class moves from sanctification to hope. Jim teaches Romans 8 on groaning "
            "and the Spirit's intercession, Ephesians on the Spirit as seal and deposit, and "
            "several texts on the Spirit's power to form endurance, patience, joy, and hope."
        ),
        "refs": [
            "Romans 8:18-30",
            "2 Corinthians 12:7-10",
            "Ephesians 1:13-14",
            "Ephesians 1:19-20",
            "Ephesians 3:16-17",
            "Colossians 1:11-12",
            "Romans 15:13",
            "Romans 14:17-18",
            "1 Corinthians 15",
            "Galatians 5:22-23",
            "Philippians 4:7",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "Romans 8:26-27",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "The Spirit helps us in weakness and intercedes with groans beyond words.",
                "url": bible_link("Romans 8:26-27"),
            },
            {
                "kind": "author",
                "source": "Francis Chan, Forgotten God",
                "status": "Verified in widely quoted excerpts and reviews of the book; the transcript paraphrases it.",
                "text": "If God truly lives in us, we should expect our lives to look different.",
                "url": "https://scottlingle.com/forgotten-god-francis-chan/",
            },
        ],
    },
    {
        "num": 8,
        "file": "hs08.txt",
        "title": "Acts Begins: Mission, Pentecost, and the Message of Jesus",
        "summary": (
            "Jim turns to Acts, where the Spirit empowers mission from Jerusalem to the ends of "
            "the earth. Pentecost is presented as a unique public event whose miraculous signs "
            "serve the Spirit-inspired message of Jesus."
        ),
        "refs": [
            "Acts 1:8",
            "Matthew 28:18-20",
            "Acts 1:1-26",
            "Acts 2:1-41",
            "Acts 9",
            "Acts 15",
            "Acts 16:6-7",
            "John 16:7",
            "Joel 2:28-32",
            "Genesis 11:1-9",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "Acts 1:8",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "You will receive power when the Holy Spirit comes on you, and you will be witnesses.",
                "url": bible_link("Acts 1:8"),
            },
            {
                "kind": "scripture",
                "source": "Acts 2:16-18",
                "status": "Peter quotes Joel; version not stated in the audio.",
                "text": "God promised to pour out his Spirit on all people.",
                "url": bible_link("Acts 2:16-18"),
            },
        ],
    },
    {
        "num": 9,
        "file": "hs09.txt",
        "title": "Samaria and the Gospel Across the First Barrier",
        "summary": (
            "Acts 8 becomes Jim's first major test case for interpreting unusual Spirit events. "
            "He argues that the Samaritan episode is not a normal conversion pattern but a unique "
            "bridge over Jewish prejudice, publicly marking Samaritans as equal recipients."
        ),
        "refs": [
            "Acts 1:8",
            "Acts 2",
            "Acts 6",
            "Acts 8:1-25",
            "2 Kings 17",
            "Daniel 1",
            "John 4",
            "Acts 10-11",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "Acts 8:12-17",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "The Samaritans believed Philip's message, were baptized, and later received the Spirit through Peter and John.",
                "url": bible_link("Acts 8:12-17"),
            },
            {
                "kind": "scripture",
                "source": "John 4:9",
                "status": "Version not stated in the audio; cited as background for Jewish-Samaritan hostility.",
                "text": "Jews did not associate with Samaritans.",
                "url": bible_link("John 4:9"),
            },
        ],
    },
    {
        "num": 10,
        "file": "hs10.txt",
        "title": "Cornelius and the Gentile Breakthrough",
        "summary": (
            "The Cornelius account in Acts 10-11 is treated as another decisive bridge. God uses "
            "visions, Peter's reluctant obedience, the Spirit's visible coming, and the church's "
            "response to show that Gentiles are received without becoming Jews."
        ),
        "refs": [
            "Acts 10:1-48",
            "Acts 11:1-18",
            "Leviticus 20:25-26",
            "Mark 7:18-19",
            "Acts 2",
            "Acts 19:1-7",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "Acts 10:34-35",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "Peter realizes that God does not show favoritism but accepts people from every nation.",
                "url": bible_link("Acts 10:34-35"),
            },
            {
                "kind": "scripture",
                "source": "Acts 11:15-18",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "Peter compares the Spirit's coming on Cornelius's household to the beginning at Pentecost.",
                "url": bible_link("Acts 11:15-18"),
            },
        ],
    },
    {
        "num": 11,
        "file": "hs11.txt",
        "title": "Acts 19, Baptism in the Holy Spirit, and Experience Tested by Scripture",
        "summary": (
            "The final transcript studies the disciples of John in Acts 19, summarizes Jim's view "
            "that salvation is an organic whole, explains baptism with the Holy Spirit as the "
            "historic outpouring begun at Pentecost, and then weighs Jim's own charismatic "
            "experience against Scripture."
        ),
        "refs": [
            "Acts 18:24-28",
            "Acts 19:1-7",
            "Galatians 3:1-5",
            "Matthew 3:11",
            "Acts 1:4-5",
            "Acts 2:16-18",
            "Acts 8",
            "Acts 10:44-48",
            "Acts 11:15-18",
            "Acts 16",
            "1 Corinthians 15:14-20",
            "Joel 2:28-32",
        ],
        "quotes": [
            {
                "kind": "scripture",
                "source": "Acts 19:1-7",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "Paul asks whether the Ephesians received the Holy Spirit when they believed, then points them from John's baptism to Jesus.",
                "url": bible_link("Acts 19:1-7"),
            },
            {
                "kind": "scripture",
                "source": "Acts 1:4-5",
                "status": "Version not stated in the audio; class wording is NIV-like.",
                "text": "John baptized with water, but the apostles would be baptized with the Holy Spirit.",
                "url": bible_link("Acts 1:4-5"),
            },
        ],
    },
]

TOPIC_INDEX = [
    ("Acts, Book of", [8, 9, 10, 11]),
    ("Acts 1:8 and Mission", [8, 9]),
    ("Acts 2 / Pentecost", [2, 3, 8, 10, 11]),
    ("Acts 8 / Samaritans", [9, 11]),
    ("Acts 10-11 / Cornelius", [9, 10, 11]),
    ("Acts 19 / Disciples of John", [10, 11]),
    ("Apollos, Aquila, and Priscilla", [11]),
    ("Apostles, Unique Witness of", [1, 2, 8]),
    ("Baptism and Conversion", [3, 4, 8, 10, 11]),
    ("Baptism in the Holy Spirit", [8, 10, 11]),
    ("Charismatic Movement", [5, 8, 9, 10, 11]),
    ("Christ-Centered Work of the Spirit", [1, 2, 3, 7, 8, 11]),
    ("Colossians and Fullness in Christ", [3, 4]),
    ("Conversion as an Organic Whole", [3, 4, 9, 10, 11]),
    ("Corinth and the Body as Temple", [4, 5, 6]),
    ("Dietary Laws and Gentile Inclusion", [10]),
    ("Ephesians: Seal, Deposit, and Power", [7]),
    ("Experiences Tested by Scripture", [1, 5, 8, 11]),
    ("Faith and Receiving the Spirit", [3, 4, 11]),
    ("Francis Chan / Forgotten God", [1, 2, 6, 7, 8]),
    ("Gentiles in the Kingdom", [3, 8, 9, 10, 11]),
    ("God the Father, Son, and Spirit", [1, 2, 5]),
    ("Great Commission", [8, 9]),
    ("Holy Spirit as Person", [1, 2]),
    ("Holy Spirit and Prayer", [1, 6, 7, 10]),
    ("Holy Spirit as Seal and Deposit", [7]),
    ("Indwelling of the Spirit", [3, 4, 5, 6, 7]),
    ("John 14-16 / Paraclete Promises", [1, 2]),
    ("John 7 and Living Water", [1, 3, 4]),
    ("John's Baptism", [10, 11]),
    ("Miracles and Extraordinary Signs", [5, 8, 9, 10, 11]),
    ("New Birth / Washing of Rebirth", [3, 4]),
    ("Old Testament Promise of the Spirit", [1, 2, 3, 8, 11]),
    ("Pentecostalism", [5, 8, 9, 10, 11]),
    ("R. A. Torrey", [1]),
    ("Romans 8", [3, 6, 7]),
    ("Samaritans", [9, 10, 11]),
    ("Sanctification", [4, 5, 6, 7, 11]),
    ("Scripture and the Spirit", [2, 6, 11]),
    ("Shema", [1, 2, 9, 10]),
    ("Speaking in Tongues", [5, 7, 8, 9, 10, 11]),
    ("The Spirit's Intercession", [7]),
    ("Titus 3", [4, 9, 11]),
    ("Toronto Blessing", [5, 6, 11]),
    ("Trinity", [1, 2, 5]),
    ("Wesleyan Perfectionism", [3, 5, 8, 9, 11]),
]

TRANSCRIPT_QUOTES: dict[int, list[dict[str, str]]] = {
    1: [
        {
            "needle": "Hear, O Israel. The Lord our God is one. Love the Lord your God with all your heart, with all your soul, and with all your strength.",
            "source": "Deuteronomy 6:4-5",
            "url": bible_link("Deuteronomy 6:4-5"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
        {
            "needle": "This is my son, whom I love, and him I am well pleased.",
            "source": "Matthew 3:16-17",
            "url": bible_link("Matthew 3:16-17"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
        {
            "needle": "Holy Spirit is a person. He is not enthusiasm. He is not courage. He is not energy. He is not personification of all good qualities",
            "source": "A. W. Tozer, The Counselor",
            "url": "https://sermoncentral.com/sermon-illustrations/2367/in-his-book-the-counselor-a-w-tozer-said-by-alan-stokes",
            "status": "Verified source for the personhood wording; the transcript paraphrases the quote.",
        },
    ],
    3: [
        {
            "needle": "And I will pour out my spirit upon all mankind.",
            "source": "Isaiah 44:3",
            "url": bible_link("Isaiah 44:3"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
    ],
    4: [
        {
            "needle": "He saved us through the washing of rebirth and renewal by the Holy Spirit.",
            "source": "Titus 3:4-7",
            "url": bible_link("Titus 3:4-7"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
    ],
    10: [
        {
            "needle": "As I began to speak, the Holy Spirit came on them as he came on us at the beginning",
            "source": "Acts 11:15-18",
            "url": bible_link("Acts 11:15-18"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
        {
            "needle": "Then I remembered the words, what the Lord had said, John baptized with water, which you will be baptized with the Holy Spirit.",
            "source": "Acts 11:15-18",
            "url": bible_link("Acts 11:15-18"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
    ],
    11: [
        {
            "needle": "John baptized with water, but just in a few days, you will be baptized with the Holy Spirit.",
            "source": "Acts 1:4-5",
            "url": bible_link("Acts 1:4-5"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
        {
            "needle": "In the last days, God says, I will pour out my spirit.",
            "source": "Acts 2:16-18",
            "url": bible_link("Acts 2:16-18"),
            "status": "Version not stated in the audio; class wording is NIV-like.",
        },
    ],
}


REPLACEMENTS: list[tuple[str, str]] = [
    (r"\bChristodum\b", "Christendom"),
    (r"\bHoly Ghost\b", "Holy Spirit"),
    (r"\bHoly\s+Spirit's temple\b", "Holy Spirit's temple"),
    (r"\bpaper weight\b", "paperweight"),
    (r"\blet's moving away\b", "then moving away"),
    (r"\bpurpose intentionally sidesteped\b", "purposely and intentionally sidestepped"),
    (r"\bsidesteped\b", "sidestepped"),
    (r"\bthose successes\b", "those excesses"),
    (r"\bthings they don't not do\b", "things they ought not do"),
    (r"\bHigh Spirit\b", "Spirit"),
    (r"\bCass for the Friendly Ghost\b", "Casper the Friendly Ghost"),
    (r"\bIt's what I lack\. Here\. Now, is there a text you can murder\?", "It means 'hear.' Now, is there a text you can remember?"),
    (r"\bHero is real\b", "Hear, O Israel"),
    (r"\bthe democrat just called it a Thomas\b", "Democritus called it atomos"),
    (r"\batom views\b", "physical"),
    (r"\bnot trainitarian\b", "not Trinitarian"),
    (r"\bHoly Rollers\b", "Holy Rollers"),
    (r"\bForgotten god\b", "Forgotten God"),
    (r"\bFrench Chan\b", "Francis Chan"),
    (r"\bFrancis Shafers\b", "Francis Schaeffer"),
    (r"\bFrancis Shafer\b", "Francis Schaeffer"),
    (r"\bFrancis Schaefer\b", "Francis Schaeffer"),
    (r"\bR\.A\. Tory\b", "R. A. Torrey"),
    (r"\bR\.A\. Torry\b", "R. A. Torrey"),
    (r"\bJack Fossil\b", "Jack Frost"),
    (r"\bJack Ross\b", "Jack Frost"),
    (r"Rogers\. Now, there's not in capitalism\.", "A. W. Tozer put it this way:"),
    (r"\bButeronomy\b", "Deuteronomy"),
    (r"\bthe Shima\b", "the Shema"),
    (r"\bShima\b", "Shema"),
    (r"\bShema is\b", "Shema is"),
    (r"\bTudy of the Holy Spirit\b", "study of the Holy Spirit"),
    (r"\bstudy in the Holy Spirit\b", "study of the Holy Spirit"),
    (r"\bcard eighth stage\b", "incarnate stage"),
    (r"\bsubanism\b", "Sabellianism"),
    (r"\bAryanism\b", "Arianism"),
    (r"\btri-theism\b", "tritheism"),
    (r"\bJohn 45 to 16\b", "John 14-16"),
    (r"\bJohn 40, 50 and 60\b", "John 14, 15, and 16"),
    (r"\b1450-16\b", "14-16"),
    (r"\bX-15\b", "Acts 15"),
    (r"\bActs of Who\b", "Acts of whom"),
    (r"\bPool salon\b", "Pool of Siloam"),
    (r"\bPulse Island\b", "Pool of Siloam"),
    (r"\bPool Siloam\b", "Pool of Siloam"),
    (r"\bWatergate\b", "Water Gate"),
    (r"\bhalal songs\b", "Hallel Psalms"),
    (r"\bFeast of Tavernacles\b", "Feast of Tabernacles"),
    (r"\bpizza tabernacles\b", "Feast of Tabernacles"),
    (r"\bspeech tabernacles\b", "Feast of Tabernacles"),
    (r"\bGalicia\b", "Galatia"),
    (r"\binvalations\b", "Galatians"),
    (r"\baorstance\b", "aorist tense"),
    (r"\bAorstance\b", "Aorist tense"),
    (r"\bworse tense\b", "aorist tense"),
    (r"\ba worse tense\b", "an aorist tense"),
    (r"\bsimple nature\b", "sinful nature"),
    (r"\bsimple life\b", "sinful life"),
    (r"\bQuarrant\b", "Corinth"),
    (r"\bQuorrant\b", "Corinth"),
    (r"\bCorridor\b", "Corinth"),
    (r"\bCore\b", "Corinth"),
    (r"\bFirst Corinthians\b", "1 Corinthians"),
    (r"\bSecond Thessalonians\b", "2 Thessalonians"),
    (r"\bFirst Thessalonians\b", "1 Thessalonians"),
    (r"\bFirst Peter\b", "1 Peter"),
    (r"\bColossian Heresy\b", "Colossian heresy"),
    (r"\bClash of 2\b", "Colossians 2"),
    (r"\bClashes to\b", "Colossians 2"),
    (r"\brecalashes\b", "Colossians"),
    (r"\bLutron\b", "loutron"),
    (r"\bLuteron\b", "loutron"),
    (r"\bluteron\b", "loutron"),
    (r"\bDury\b", "During"),
    (r"\bWesterly\b", "Wesley"),
    (r"\bWestern imperfections\b", "Wesleyan perfectionism"),
    (r"\bWussleys\b", "Wesley's"),
    (r"\bWesley Brock\b", "Wesley had"),
    (r"\bCharles G\. Finney\b", "Charles G. Finney"),
    (r"\bAgna's Osment\b", "Agnes Ozman"),
    (r"\bFox parham, Bethel Bible School\b", "Charles Parham's Bethel Bible School"),
    (r"\bfull gospel business men's\b", "Full Gospel Business Men's"),
    (r"\bToronto Blustling\b", "Toronto Blessing"),
    (r"\bToronto blessing\b", "Toronto Blessing"),
    (r"\bswoon in the spirit\b", "slain in the Spirit"),
    (r"\bspoon in the spirit\b", "slain in the Spirit"),
    (r"\bsmoothing in the spirit\b", "slain in the Spirit"),
    (r"\bholy copper\b", "holy helicopter"),
    (r"\btongue speaking\b", "speaking in tongues"),
    (r"\btongue-speaking\b", "speaking in tongues"),
    (r"\bspeaking intungs\b", "speaking in tongues"),
    (r"\bspeaking in time\b", "speaking in tongues"),
    (r"\bspeaking times\b", "speaking in tongues"),
    (r"\bspeaking and done\b", "speaking in tongues"),
    (r"\bBabs and Holy Spirit\b", "baptism in the Holy Spirit"),
    (r"\bBaptist Mollie Spirit\b", "baptism in the Holy Spirit"),
    (r"\bbachelors Holy Spirit\b", "baptism in the Holy Spirit"),
    (r"\bbavi's Holy Spirit\b", "baptism in the Holy Spirit"),
    (r"\bgiftfully spirit\b", "baptism in the Holy Spirit"),
    (r"\bBaptism Holy Spirit\b", "baptism in the Holy Spirit"),
    (r"\bBaptismally Spirit\b", "baptism in the Holy Spirit"),
    (r"\breceiving about the Holy Spirit\b", "receiving the baptism in the Holy Spirit"),
    (r"\bSesteria\b", "Caesarea"),
    (r"\bSesterea\b", "Caesarea"),
    (r"\bSusereo\b", "Caesarea"),
    (r"\bSireen\b", "Cyrene"),
    (r"\bPaulus\b", "Apollos"),
    (r"\bA Paulos\b", "Apollos"),
    (r"\bApollo\b", "Apollos"),
    (r"\bPaulist's activity\b", "Apollos's activity"),
    (r"\bApollo goes to Koran\b", "Apollos goes to Corinth"),
    (r"\bKoran\b", "Corinth"),
    (r"\ba Quill and Priscilla\b", "Aquila and Priscilla"),
    (r"\bQuill and Priscilla\b", "Aquila and Priscilla"),
    (r"\ban X 19\b", "Acts 19"),
    (r"\bX 19\b", "Acts 19"),
    (r"\baggressive aorus\b", "ingressive aorist"),
    (r"\baorus\b", "aorist"),
    (r"\bdiscursory devotional\b", "cursory devotional"),
    (r"\bsin structure\b", "sentence structure"),
    (r"\bdeathbaral resurrection\b", "death, burial, and resurrection"),
    (r"\bmission of sins\b", "remission of sins"),
    (r"\bbackaised\b", "baptized"),
    (r"\bRegulations 3\b", "Galatians 3"),
    (r"\bActs 10-11\b", "Acts 10-11"),
    (r"\ba kale and eat\b", "kill and eat"),
    (r"\bsuffer time\b", "supper time"),
    (r"\bcomes out of the trans\b", "comes out of the trance"),
    (r"\bSimon and Tanner\b", "Simon the tanner"),
    (r"\bproselyt\b", "proselyte"),
    (r"\bCongress actually\b", "converts actually"),
    (r"\bthe Sclepius\b", "Asclepius"),
    (r"\bprophodite\b", "Aphrodite"),
    (r"\bUnic\b", "eunuch"),
    (r"\bFlippy and Jailer\b", "Philippian jailer"),
    (r"\bJenny Buckingham\b", "Jamie Buckingham"),
    (r"\bBob Winer\b", "Bob Weiner"),
    (r"\bMagnoia Street\b", "Magnolia Street"),
    (r"\bproselyt baptism\b", "proselyte baptism"),
    (r"\bdebouchery\b", "debauchery"),
    (r"\bdevo\b", "devo"),
    (r"\bMaranatha\b", "Maranatha"),
]


STARTERS = (
    "Now ",
    "So ",
    "Then ",
    "First ",
    "Second ",
    "Third ",
    "Finally ",
    "Notice ",
    "Remember ",
    "Let's ",
    "What ",
    "Why ",
    "How ",
    "Okay",
    "All right",
    "In other words",
    "By the way",
    "The point",
)


def clean_line(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    if re.fullmatch(r"[.\s]+", line):
        return ""
    line = re.sub(r"\s+", " ", line)
    line = line.replace("’", "'").replace("“", '"').replace("”", '"')
    line = line.replace("—", "-").replace("–", "-")
    for pattern, replacement in REPLACEMENTS:
        line = re.sub(pattern, replacement, line, flags=re.IGNORECASE if pattern.islower() else 0)
    line = re.sub(r"\b(and|or|the|that|this|you|we|he|she|it)(?:\s+\1\b){2,}", r"\1", line, flags=re.I)
    line = re.sub(r"\b(you know,\s*){2,}", "you know, ", line, flags=re.I)
    line = re.sub(r"\s+([,.?!;:])", r"\1", line)
    line = re.sub(r"([,.?!;:])([A-Za-z])", r"\1 \2", line)
    return line


def ends_sentence(text: str) -> bool:
    """Return true when a transcript line ends at a natural paragraph boundary."""
    return bool(re.search(r"[.!?][\"')\]]?$", text))


def split_paragraphs(text: str) -> list[str]:
    return [para.strip() for para in text.split("\n\n") if para.strip()]


def transcript_quote_for(class_num: int, paragraph: str) -> dict[str, str] | None:
    for quote in TRANSCRIPT_QUOTES.get(class_num, []):
        if quote["needle"].lower() in paragraph.lower():
            return quote
    return None


def paragraph_anchor(num: int, para_num: int) -> str:
    return f"{class_anchor(num)}-p{para_num:03d}"


def format_transcript_paragraph(class_num: int, para_num: int, paragraph: str) -> str:
    anchor = paragraph_anchor(class_num, para_num)
    quote = transcript_quote_for(class_num, paragraph)
    if quote:
        cite = md_link(quote["source"], quote["url"])
        block = (
            f"::: {{#{anchor}}}\n"
            f"> {paragraph}\n"
            ">\n"
            f"> -- {cite}. {quote['status']}\n"
            ":::"
        )
        return block
    return f"::: {{#{anchor}}}\n{paragraph}\n:::"


def clean_text(path: Path) -> str:
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lines = [clean_line(line) for line in raw_lines]
    lines = [line for line in lines if line]

    paragraphs: list[str] = []
    current: list[str] = []
    current_words = 0
    for line in lines:
        words = len(line.split())
        has_boundary = bool(current and ends_sentence(current[-1]))
        starts_new = current_words >= 90 and has_boundary and line.startswith(STARTERS)
        too_long = current_words >= 145 and has_boundary
        if current and (starts_new or too_long):
            paragraphs.append(" ".join(current))
            current = []
            current_words = 0
        current.append(line)
        current_words += words

    if current:
        paragraphs.append(" ".join(current))

    text = "\n\n".join(paragraphs)
    text = re.sub(r"\bJesus Christ\b", "Jesus Christ", text)
    text = re.sub(r"\bHoly Spirit\b", "Holy Spirit", text)
    text = re.sub(r"\bGod's Spirit\b", "God's Spirit", text)
    text = re.sub(r"^all the effects", "All the effects", text)
    text = re.sub(
        r"^18 before you arrived at Acts 19",
        "At the end of Acts 18, before you arrive at Acts 19",
        text,
    )
    text = text.replace("Then it says that Apollos\n\ngoes to Corinth.", "Then it says that Apollos goes to Corinth.")
    text = text.replace("a Apollos's activity", "Apollos' activity")
    text = text.replace("Apollos's activity", "Apollos' activity")
    if path.name == "hs11.txt":
        text = text.replace(
            "And it says once when he was eating with them, he commanded them, do not leave Jerusalem until the Father sends you the gift he promised.",
            "And it says:\n\nonce when he was eating with them, he commanded them, do not leave Jerusalem until the Father sends you the gift he promised.",
        )
        text = text.replace(
            "And those to phrase the Joel uses. In the last days, God says, I will pour out my spirit.",
            "And those to phrase the Joel uses.\n\nIn the last days, God says, I will pour out my spirit.",
        )
        text = text.replace(
            "In the last days, God says, I will pour out my spirit.\n\nUpon all people",
            "In the last days, God says, I will pour out my spirit. Upon all people",
        )
        text = text.replace(
            "they will prophesy. Now, what I want you to see here",
            "they will prophesy.\n\nNow, what I want you to see here",
        )
    return text.strip()


def md_link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def ref_item(ref: str) -> str:
    return f"- {md_link(ref, bible_link(ref))}"


def quote_block(q: dict[str, str]) -> str:
    source = q["source"]
    status = q["status"]
    url = q.get("url", "")
    cite = md_link(source, url) if url else source
    return (
        f"> {q['text']}\n>\n"
        f"> -- {cite}. {status}"
    )


def class_anchor(num: int) -> str:
    return f"class-{num:02d}"


def make_class_markdown(meta: dict, transcript_paragraphs: list[str], master: bool = False) -> str:
    num = meta["num"]
    title = meta["title"]
    heading_level = "##" if master else "#"
    heading = f"{heading_level} Class {num}: {title}"
    if master:
        heading += f" {{#{class_anchor(num)}}}"

    refs = "\n".join(ref_item(ref) for ref in meta["refs"])
    quotes = "\n\n".join(quote_block(q) for q in meta.get("quotes", []))
    if not quotes:
        quotes = "_No direct author quote was isolated in this class transcript._"

    transcript = "\n\n".join(
        format_transcript_paragraph(num, para_num, paragraph)
        for para_num, paragraph in enumerate(transcript_paragraphs, start=1)
    )

    return "\n\n".join(
        [
            heading,
            f"**Original transcript:** `{meta['file']}`",
            f"**Summary:** {meta['summary']}",
            "### Key Scripture References",
            refs,
            "### Quotations and Source Notes",
            quotes,
            "### Cleaned Transcript",
            transcript,
        ]
    ).strip() + "\n"


def make_intro() -> str:
    toc_rows = [
        "| Class | Source File | Title | Summary |",
        "|---:|---|---|---|",
    ]
    for meta in CLASSES:
        num = meta["num"]
        toc_rows.append(
            "| "
            f"{md_link(str(num), '#' + class_anchor(num))} "
            f"| `{meta['file']}` "
            f"| {meta['title']} "
            f"| {meta['summary']} |"
        )

    index: dict[str, list[int]] = defaultdict(list)
    for meta in CLASSES:
        for ref in meta["refs"]:
            index[ref].append(meta["num"])

    def sort_key(ref: str) -> tuple[int, str]:
        order = [
            "Genesis",
            "Exodus",
            "Leviticus",
            "Numbers",
            "Deuteronomy",
            "Joshua",
            "Judges",
            "Ruth",
            "1 Samuel",
            "2 Samuel",
            "1 Kings",
            "2 Kings",
            "Psalms",
            "Psalm",
            "Proverbs",
            "Isaiah",
            "Jeremiah",
            "Daniel",
            "Joel",
            "Matthew",
            "Mark",
            "Luke",
            "John",
            "Acts",
            "Romans",
            "1 Corinthians",
            "2 Corinthians",
            "Galatians",
            "Ephesians",
            "Philippians",
            "Colossians",
            "1 Thessalonians",
            "2 Thessalonians",
            "Titus",
            "1 Peter",
        ]
        for i, book in enumerate(order):
            if ref.startswith(book):
                return (i, ref)
        return (999, ref)

    index_rows = [
        "| Scripture | Discussed In | External Passage |",
        "|---|---|---|",
    ]
    for ref in sorted(index, key=sort_key):
        classes = ", ".join(md_link(f"Class {n}", f"#{class_anchor(n)}") for n in index[ref])
        index_rows.append(f"| {ref} | {classes} | {md_link('Open passage', bible_link(ref))} |")

    quote_rows = [
        "| Source | Verification Note | Classes |",
        "|---|---|---|",
    ]
    seen: dict[str, tuple[str, set[int], str]] = {}
    for meta in CLASSES:
        for q in meta.get("quotes", []):
            if q["kind"] == "author":
                key = q["source"]
                if key not in seen:
                    seen[key] = (q["status"], set(), q.get("url", ""))
                seen[key][1].add(meta["num"])
    for source, (status, nums, url) in seen.items():
        source_label = md_link(source, url) if url else source
        classes = ", ".join(md_link(f"Class {n}", f"#{class_anchor(n)}") for n in sorted(nums))
        quote_rows.append(f"| {source_label} | {status} | {classes} |")

    front_matter = "\n".join(
        [
            "---",
            f"title: \"{TITLE}\"",
            f"subtitle: \"{SUBTITLE}\"",
            "author: \"Jim Brinkerhoff\"",
            "---",
        ]
    )

    return "\n\n".join(
        [
            front_matter,
            f"# {TITLE}",
            f"**{SUBTITLE}**",
            (
                "These files are edited from Whisper AI transcriptions of eleven Bible classes. "
                "The cleanup preserves the informal cadence of a live class while correcting obvious "
                "transcription errors, adding structure, and identifying major Scripture references. "
                "Bible quotations are set off in source notes when the passage is clearly being quoted; "
                "the audio does not consistently identify a translation, so most are marked as NIV-like "
                "or version not stated."
            ),
            "## Table of Contents",
            "\n".join(toc_rows),
            "## Scripture Index {#scripture-index}",
            "\n".join(index_rows),
            "## Quote Verification Notes {#quote-verification-notes}",
            "\n".join(quote_rows),
        ]
    )


TOPIC_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "book",
    "class",
    "in",
    "of",
    "or",
    "the",
    "to",
    "with",
    "on",
    "by",
    "for",
}


def topic_terms(topic: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9']+", topic.lower())
    return [w for w in words if w not in TOPIC_STOPWORDS and len(w) > 1]


def score_topic_paragraph(topic: str, paragraph: str) -> int:
    text = paragraph.lower()
    if topic.lower() in text:
        return 100
    score = 0
    for term in topic_terms(topic):
        if term in text:
            score += 1
    return score


def best_topic_anchor(topic: str, class_num: int, paragraphs: list[str]) -> tuple[str, int]:
    best_para = 1
    best_score = -1
    for para_num, paragraph in enumerate(paragraphs, start=1):
        score = score_topic_paragraph(topic, paragraph)
        if score > best_score:
            best_score = score
            best_para = para_num
    return paragraph_anchor(class_num, best_para), best_para


def make_topic_index(paragraphs_by_class: dict[int, list[str]]) -> str:
    rows = [
        "| Topic | Discussed In |",
        "|---|---|",
    ]
    for topic, class_nums in sorted(TOPIC_INDEX, key=lambda item: item[0].lower()):
        links: list[str] = []
        for num in class_nums:
            anchor, para_num = best_topic_anchor(topic, num, paragraphs_by_class[num])
            links.append(md_link(f"Class {num} ¶{para_num}", f"#{anchor}"))
        links_str = ", ".join(links)
        rows.append(f"| {topic} | {links_str} |")

    return "\n\n".join(
        [
            "\\newpage",
            "## Topic Index {#topic-index}",
            (
                "This index groups recurring themes across the eleven classes. "
                "Each class reference links to a specific paragraph where that topic is discussed."
            ),
            "\n".join(rows),
        ]
    )


def write_css() -> None:
    CSS_OUT.write_text(
        """
:root {
  --ink: #242721;
  --muted: #687064;
  --paper: #f7f4ed;
  --panel: #fffdf8;
  --panel-soft: #f0ece2;
  --line: #ddd7cb;
  --line-strong: #c9bead;
  --green: #183c34;
  --green-2: #2d6658;
  --gold: #b87932;
  --link: #1f6687;
  --shadow: 0 18px 45px rgba(45, 40, 30, .09);
}

* { box-sizing: border-box; }
html {
  scroll-behavior: smooth;
  background: var(--paper);
}

body {
  margin: 0;
  background:
    linear-gradient(180deg, #eee8dc 0, var(--paper) 340px),
    var(--paper);
  color: var(--ink);
  font-family: Charter, "Iowan Old Style", "Source Serif Pro", Georgia, Cambria, "Times New Roman", serif;
  font-size: 18.5px;
  line-height: 1.72;
  text-rendering: optimizeLegibility;
}

body > * {
  width: min(100% - 2rem, 76ch);
  margin-left: auto;
  margin-right: auto;
}

h1, h2, h3 {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.18;
  letter-spacing: 0;
  text-wrap: balance;
}

h1 {
  font-size: 2.75rem;
  margin-top: 3rem;
  margin-bottom: .7rem;
  color: #172a25;
}

h2 {
  font-size: 1.9rem;
  margin-top: 4.2rem;
  margin-bottom: 1rem;
  padding-top: 1.1rem;
  border-top: 1px solid var(--line-strong);
  color: #172a25;
}

h3 {
  font-size: 1rem;
  margin-top: 2.2rem;
  margin-bottom: .7rem;
  color: var(--green);
  text-transform: uppercase;
  letter-spacing: .06em;
}

a {
  color: var(--link);
  text-decoration-thickness: .07em;
  text-underline-offset: .18em;
}

a:hover { color: var(--green-2); }
p { margin: 1rem 0; }
strong { font-weight: 700; }

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: .86em;
  background: #ece6da;
  padding: .1em .35em;
  border-radius: 5px;
}

#title-block-header {
  width: 100%;
  max-width: none;
  margin: 0 0 2rem;
  padding: 4.6rem max(1.25rem, calc((100vw - 76ch) / 2)) 3.2rem;
  background:
    linear-gradient(135deg, rgba(24, 60, 52, .97), rgba(45, 102, 88, .94)),
    #183c34;
  color: #fffaf0;
}

#title-block-header .title {
  max-width: 13ch;
  margin: 0;
  color: #fffaf0;
  font-size: 3.25rem;
  line-height: 1.04;
}

#title-block-header .subtitle {
  max-width: 48rem;
  margin: 1rem 0 0;
  color: rgba(255, 250, 240, .86);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 1.05rem;
  line-height: 1.5;
}

#title-block-header .author {
  margin: .45rem 0 0;
  color: rgba(255, 250, 240, .68);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .92rem;
}

#the-holy-spirit-eleven-bible-classes {
  display: none;
}

#the-holy-spirit-eleven-bible-classes + p {
  margin-top: 0;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

blockquote {
  margin: 1.6rem 0;
  padding: 1.05rem 1.15rem 1.05rem 1.25rem;
  border-left: .22rem solid var(--gold);
  border-radius: 0 8px 8px 0;
  background: var(--panel);
  box-shadow: 0 1px 0 rgba(0,0,0,.035);
}

blockquote p { margin: .5rem 0; }

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 1.2rem 0 2.4rem;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .9rem;
  line-height: 1.48;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 0 rgba(0,0,0,.03);
}

th, td {
  border: 0;
  border-bottom: 1px solid var(--line);
  padding: .7rem .78rem;
  vertical-align: top;
}

tbody tr:last-child td { border-bottom: 0; }
tbody tr:nth-child(even) td { background: #faf7ef; }

th {
  text-align: left;
  background: #e9e0cf;
  color: #26322c;
  font-size: .82rem;
  text-transform: uppercase;
  letter-spacing: .04em;
}

#TOC {
  width: min(100% - 2rem, 76ch);
  margin: -1rem auto 2.2rem;
  background: rgba(255, 253, 248, .94);
  color: var(--ink);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .94rem;
  line-height: 1.35;
  padding: 1rem;
  border: 1px solid var(--line);
  border-radius: 10px;
  box-shadow: var(--shadow);
}

#TOC::before {
  content: "Contents";
  display: block;
  margin: 0 0 .55rem;
  color: var(--muted);
  font-size: .76rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
}

#TOC a {
  color: #26322c;
  text-decoration: none;
}

#TOC a:hover { color: var(--link); }
#TOC ul { list-style: none; padding-left: .85rem; margin: .3rem 0; }
#TOC > ul { padding-left: 0; }
#TOC li { margin: .34rem 0; }
#TOC > ul > li > a { display: none; }
.toc-toggle {
  display: none;
}

@media (min-width: 1120px) {
  body {
    display: grid;
    grid-template-columns: 300px minmax(0, 78ch);
    column-gap: 3.2rem;
    align-items: start;
    justify-content: center;
  }

  #title-block-header {
    grid-column: 1 / -1;
    margin-bottom: 0;
  }

  #TOC {
    grid-column: 1;
    position: sticky;
    top: 1.2rem;
    width: auto;
    margin: 2rem 0 0;
    max-height: calc(100vh - 2.4rem);
    overflow: auto;
    box-shadow: var(--shadow);
  }

  body > :not(#TOC):not(#title-block-header) {
    grid-column: 2;
    width: 100%;
    margin-left: 0;
    margin-right: auto;
  }

  h1 { margin-top: 3rem; }
}

@media (max-width: 760px) {
  body {
    font-size: 17px;
    line-height: 1.68;
  }

  body > * {
    width: min(100% - 1rem, 76ch);
  }

  #title-block-header {
    padding: 3rem 1rem 2.2rem;
    margin-bottom: 1rem;
  }

  #title-block-header .title {
    max-width: 12ch;
    font-size: 2.35rem;
  }

  #title-block-header .subtitle {
    font-size: .98rem;
  }

  #TOC {
    position: sticky;
    top: 0;
    z-index: 20;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 2.75rem;
    align-items: center;
    gap: .65rem;
    width: 100%;
    max-height: none;
    margin: 0 0 1.6rem;
    padding: .55rem .75rem;
    border-left: 0;
    border-right: 0;
    border-radius: 0;
    overflow: visible;
    box-shadow: 0 8px 24px rgba(45, 40, 30, .12);
  }

  #TOC::before {
    margin: 0;
    color: #26322c;
    font-size: .86rem;
    letter-spacing: .07em;
  }

  .toc-toggle {
    appearance: none;
    width: 2.75rem;
    height: 2.75rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--line-strong);
    border-radius: 8px;
    background: var(--panel);
    color: var(--green);
    cursor: pointer;
  }

  .toc-toggle span,
  .toc-toggle::before,
  .toc-toggle::after {
    content: "";
    display: block;
    width: 1.25rem;
    height: 2px;
    border-radius: 999px;
    background: currentColor;
  }

  .toc-toggle span {
    margin: 4px 0;
  }

  #TOC ul {
    display: none;
  }

  body.toc-open #TOC {
    max-height: 78vh;
    overflow: auto;
  }

  body.toc-open #TOC ul {
    display: block;
    grid-column: 1 / -1;
    width: 100%;
    max-height: calc(78vh - 4.8rem);
    margin: .15rem 0 0;
    padding-top: .65rem;
    border-top: 1px solid var(--line);
    overflow: auto;
  }

  body.toc-open #TOC li {
    margin: .48rem 0;
  }

  h1 {
    font-size: 2.05rem;
    margin-top: 2.2rem;
  }

  h2 {
    font-size: 1.45rem;
    margin-top: 3rem;
  }

  h3 { font-size: .9rem; }

  table {
    display: block;
    overflow-x: auto;
    white-space: normal;
    border-radius: 8px;
  }

  th, td {
    min-width: 9rem;
    padding: .62rem .68rem;
  }

  blockquote {
    margin-left: 0;
    margin-right: 0;
  }
}

@media print {
  body { background: white; font-size: 11.5pt; }
  #TOC { color: var(--ink); background: white; position: static; height: auto; }
  #TOC a { color: var(--ink); }
  body > * { max-width: none; }
  h2 { break-before: page; }
  table { font-size: 9pt; }
  a { color: var(--ink); }
}
""".strip()
        + "\n",
        encoding="utf-8",
    )


TOC_SCRIPT = """
<script>
(function () {
  var toc = document.getElementById("TOC");
  if (!toc) return;

  var button = document.createElement("button");
  button.className = "toc-toggle";
  button.type = "button";
  button.setAttribute("aria-controls", "TOC");
  button.setAttribute("aria-expanded", "false");
  button.setAttribute("aria-label", "Open contents");
  button.innerHTML = "<span></span>";
  toc.insertBefore(button, toc.firstChild);

  function setOpen(open) {
    document.body.classList.toggle("toc-open", open);
    button.setAttribute("aria-expanded", open ? "true" : "false");
    button.setAttribute("aria-label", open ? "Close contents" : "Open contents");
  }

  button.addEventListener("click", function () {
    setOpen(!document.body.classList.contains("toc-open"));
  });

  toc.addEventListener("click", function (event) {
    if (event.target.closest("a")) setOpen(false);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen(false);
  });
})();
</script>
""".strip()


def inject_html_script() -> None:
    html_text = HTML_OUT.read_text(encoding="utf-8")
    if TOC_SCRIPT in html_text:
        return
    HTML_OUT.write_text(html_text.replace("</body>", f"{TOC_SCRIPT}\n</body>"), encoding="utf-8")


def run_pandoc() -> None:
    html_cmd = [
        "pandoc",
        str(MASTER_MD),
        "--from",
        "markdown+pipe_tables+header_attributes+raw_tex+yaml_metadata_block",
        "--to",
        "html5",
        "--standalone",
        "--toc",
        "--toc-depth=2",
        "--embed-resources",
        "--css",
        str(CSS_OUT),
        "--metadata",
        f"title={TITLE}",
        "-o",
        str(HTML_OUT),
    ]
    subprocess.run(html_cmd, check=True, cwd=ROOT)
    inject_html_script()

    pdf_cmd = [
        "pandoc",
        str(MASTER_MD),
        "--from",
        "markdown+pipe_tables+header_attributes+raw_tex+yaml_metadata_block",
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2",
        "-V",
        "geometry:margin=0.8in",
        "-V",
        "fontsize=11pt",
        "-V",
        "linkcolor=blue",
        "-V",
        "urlcolor=blue",
        "--metadata",
        f"title={TITLE}",
        "-o",
        str(PDF_OUT),
    ]
    subprocess.run(pdf_cmd, check=True, cwd=ROOT)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CLASS_DIR.mkdir(parents=True, exist_ok=True)
    write_css()

    master_parts = [make_intro()]
    paragraphs_by_class: dict[int, list[str]] = {}

    for meta in CLASSES:
        transcript = clean_text(TXT_DIR / meta["file"])
        transcript_paragraphs = split_paragraphs(transcript)
        paragraphs_by_class[meta["num"]] = transcript_paragraphs
        class_md = make_class_markdown(meta, transcript_paragraphs, master=False)
        class_path = CLASS_DIR / f"class-{meta['num']:02d}.md"
        class_path.write_text(class_md, encoding="utf-8")

        master_parts.append("\\newpage\n\n" + make_class_markdown(meta, transcript_paragraphs, master=True))

    master_parts.append(make_topic_index(paragraphs_by_class))

    MASTER_MD.write_text("\n\n".join(master_parts), encoding="utf-8")
    run_pandoc()


if __name__ == "__main__":
    main()
