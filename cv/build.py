"""
Build the two role-specific CVs (XR and Software/AI) as polished, text-selectable
PDFs with a dark sidebar + main-column layout. Run:  python3 build.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, FrameBreak,
    NextPageTemplate, HRFlowable, KeepTogether,
)

HERE = Path(__file__).resolve().parent
PAGE_W, PAGE_H = A4

# ----- palette -------------------------------------------------------------
INK = colors.HexColor("#141a2e")       # main text
MUTED = colors.HexColor("#5a6478")     # secondary text
LINE = colors.HexColor("#e2e7f0")      # hairlines
SIDE_TXT = colors.HexColor("#d9def2")  # sidebar body text
SIDE_DIM = colors.HexColor("#9aa3c7")  # sidebar dim text
WHITE = colors.white

THEMES = {
    "xr":          {"accent": colors.HexColor("#7c5cff"), "side": colors.HexColor("#17123a"),
                    "side2": colors.HexColor("#b7a6ff"), "label": "XR / SPATIAL COMPUTING & GAME ENGINEER"},
    "software-ai": {"accent": colors.HexColor("#5b5ef0"), "side": colors.HexColor("#121634"),
                    "side2": colors.HexColor("#a9b2ff"), "label": "SENIOR FULL-STACK / AI SOFTWARE ENGINEER"},
}

# ----- geometry ------------------------------------------------------------
SIDE_W = 64 * mm                 # full-bleed sidebar band width
TOP = 15 * mm
BOT = 14 * mm
SIDE_PAD_L = 9 * mm
SIDE_INNER = SIDE_W - SIDE_PAD_L - 7 * mm
MAIN_X = SIDE_W + 8 * mm
MAIN_W = PAGE_W - MAIN_X - 13 * mm
BAND = 14 * mm                   # header band on page 2+

CONTACT = (
    "Accra, Ghana", "manteycaleb@gmail.com", "+233 57 887 6149",
)
LINKS = [
    ("Portfolio", "https://caleb-mantey.github.io/"),
    ("GitHub", "https://github.com/Caleb-Mantey"),
    ("LinkedIn", "https://www.linkedin.com/in/caleb-mantey-a461a9148/"),
    ("YouTube", "https://www.youtube.com/@CalebMantey"),
]


def styles(theme):
    acc = theme["accent"]
    return {
        # sidebar
        "name":   ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=20, leading=22, textColor=WHITE, spaceAfter=2),
        "role":   ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=8.2, leading=11, textColor=theme["side2"], spaceAfter=10, tracking=0.5),
        "s_head": ParagraphStyle("s_head", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=WHITE, spaceBefore=11, spaceAfter=5),
        "s_body": ParagraphStyle("s_body", fontName="Helvetica", fontSize=8.2, leading=11.6, textColor=SIDE_TXT, spaceAfter=3),
        "s_lbl":  ParagraphStyle("s_lbl", fontName="Helvetica-Bold", fontSize=8.1, leading=11, textColor=theme["side2"], spaceBefore=4, spaceAfter=1),
        "s_val":  ParagraphStyle("s_val", fontName="Helvetica", fontSize=8.1, leading=11.3, textColor=SIDE_TXT, spaceAfter=2),
        "s_dim":  ParagraphStyle("s_dim", fontName="Helvetica", fontSize=7.8, leading=10.8, textColor=SIDE_DIM, spaceAfter=2),
        # main
        "m_head": ParagraphStyle("m_head", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=acc, spaceBefore=8, spaceAfter=2),
        "body":   ParagraphStyle("body", fontName="Helvetica", fontSize=9, leading=12.2, textColor=INK, spaceAfter=2),
        "job":    ParagraphStyle("job", fontName="Helvetica-Bold", fontSize=9.6, leading=11.8, textColor=INK, spaceBefore=5, spaceAfter=0),
        "meta":   ParagraphStyle("meta", fontName="Helvetica-Oblique", fontSize=8.1, leading=10.8, textColor=acc, spaceAfter=2),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=8.8, leading=11.7, textColor=INK, leftIndent=9, firstLineIndent=-9, spaceAfter=1.5),
        "proj":   ParagraphStyle("proj", fontName="Helvetica", fontSize=8.8, leading=11.7, textColor=INK, leftIndent=9, firstLineIndent=-9, spaceAfter=2.5),
        # grouped project list (XR CV, page 2)
        "p_group": ParagraphStyle("p_group", fontName="Helvetica-Bold", fontSize=8.4, leading=11, textColor=acc, spaceBefore=7, spaceAfter=3, keepWithNext=1),
        "proj2":  ParagraphStyle("proj2", fontName="Helvetica", fontSize=8.7, leading=11.7, textColor=INK, spaceAfter=4.5),
    }


DATA = {
    "xr": {
        "summary": "XR & game developer, Co-Founder/CTO of Relu Interactives, and lead engineer of Relu Spatial. "
                   "I have built immersive technology in Africa since 2016: filmed 360° VR experiences, VR and "
                   "mixed-reality training on Meta Quest, industrial digital twins, brand-activation VR, multiplayer "
                   "3D, and games in Unity and the browser. My work includes Cocoa 360 for the University of Ghana, "
                   "GhanaCedi@60 VR for First National Bank, the VIVaTS digital twin for Ghana National Gas, and VR "
                   "experiences for Coca-Cola, Closeup and Standard Chartered Ghana. "
                   "I studied Geomatic Engineering, so I bring training in spatial data and coordinate systems, "
                   "the same math XR runs on.",
        "skills": [
            ("XR & real-time 3D", "Unity, C#, Meta Quest & Apple Vision Pro SDKs, OpenXR, WebXR, Three.js, React Three Fiber"),
            ("Immersive media", "360° video VR, VR storytelling, mixed reality (passthrough, hand tracking), mobile AR"),
            ("Multiplayer", "Photon, WebRTC, rollback netcode, shared sessions and voice"),
            ("Spatial systems", "Simulation, digital twins, 3D interaction, GIS & spatial data"),
            ("Engineering", "TypeScript, React, Node.js, Blender, performance optimization"),
            ("Leadership", "Technical direction, team leadership, product delivery, public speaking"),
        ],
        "experience": [
            ("Relu Interactives", "Co-Founder & CTO", "Sep 2022 – Present", [
                "Built Relu Spatial end-to-end, from backend services to the real-time XR engine, enabling AI-assisted 3D creation and cross-device publishing to web, mobile, and headsets.",
                "Built Cocoa 360 for the University of Ghana (2025): a VR experience filmed in 360° on Ghanaian cocoa farms that shows how cocoa is grown and produced.",
                "Built GhanaCedi@60 VR for First National Bank with Streamline360 (2025): a narrative VR journey through four eras of Ghana’s currency.",
                "Built PetSim and its Meta Quest 3 mixed-reality build, a drilling-rig training simulation endorsed by five Ghanaian universities and free to students; it anchored Relu’s 2023 NEIP Presidential Pitch win.",
                "Delivered VIVaTS, an operator-training and live-monitoring digital twin of national gas infrastructure for Ghana National Gas Company.",
                "Build Relu’s games: SortJam VR, Africa’s Legends VR with Leti Arts, and AKOFENA, a free online fighting game.",
                "Lead cross-disciplinary teams (engineering, 3D art, design) from prototype to delivery; represent the company in industry talks and workshops.",
            ]),
            ("Andela / client projects", "Software Engineer, Web 3D & Games", "Sep 2021 – Jan 2024", [
                "Built and ported browser-based 3D games for crypto and Telegram platforms; wired gameplay into server-side logic with client teams and fixed scaling problems.",
            ]),
            ("Soko Aerial Signal Training School", "AR / VR Developer & Researcher", "Sep 2019 – Aug 2020", [
                "Built AR and VR training experiences for new military recruits in Unity and Blender; mentored junior developers.",
            ]),
        ],
        "projects_title": "XR, VR & game projects",
        # (group, [(name, client / context, description, [(link label, url)])])
        "project_groups": [
            ("360° video & narrative VR", [
                ("Cocoa 360 VR", "University of Ghana · 2025",
                 "A VR experience filmed in 360° on cocoa farms in Ghana. It shows how cocoa is grown, harvested and processed, so viewers stand on the farm instead of reading about it. Footage on request.", []),
                ("GhanaCedi@60 VR", "First National Bank, with Streamline360 · 2025",
                 "A commemorative VR journey through 60 years of the Ghana Cedi, from cowry shells and the shilling to the old and new cedi, each era rebuilt as a place.",
                 [("reluinteractives.com/studios/ghanacedi", "https://reluinteractives.com/studios/ghanacedi")]),
            ]),
            ("VR experiences & VR games", [
                ("Coca-Cola VR Soccer Shootout", "Brand activations · Meta Quest",
                 "A VR penalty shootout with realistic physics and leaderboards, played by more than 500 people at live brand activations.",
                 [("Watch", "https://www.youtube.com/watch?v=9YB0R8QwzdE&t=30s")]),
                ("Closeup VR", "Unilever brand activation · Meta Quest",
                 "A VR experience built for a Closeup brand activation.",
                 [("LinkedIn post", "https://www.linkedin.com/posts/caleb-mantey-a461a9148_closeup-rumble5-unilever-activity-6953919923458838528-qMD5")]),
                ("Standard Chartered Ghana VR tour", "Standard Chartered Ghana · Meta Quest",
                 "A VR virtual tour, with a version you can play in the browser.",
                 [("itch.io", "https://caleb-mantey.itch.io/standard-chartered-ghana-virtual-tour")]),
                ("Virtual Exhibition", "Multi-user VR · Unity, Photon, WebRTC",
                 "A shared VR space with real-time collaboration, shared interactions and voice.", []),
                ("SortJam VR", "Relu original · in development",
                 "A physics-based VR sorting game across farm, hospital, workshop and ice-cream worlds, with timed challenges.",
                 [("reluinteractives.com/studios/sort-jam", "https://reluinteractives.com/studios/sort-jam")]),
                ("Africa’s Legends VR", "With Leti Arts",
                 "VR adaptation of the African superhero franchise: worlds, combat and the headset release for heroes drawn from African folklore.",
                 [("reluinteractives.com/studios/africa-legends", "https://reluinteractives.com/studios/africa-legends")]),
                ("Relu Spatial VR games", "Playable in a Meta Quest browser",
                 "Hoops Arena, Slice Rush, Range Rivals and Mixed Reality Counters Ball, built on Relu Spatial.",
                 [("reluspatial.com/browse", "https://reluspatial.com/browse")]),
            ]),
            ("Training, simulation & digital twins", [
                ("PetSim + PetSim MR", "Ghanaian universities · NEIP 2023 winner",
                 "Drilling-rig training covering the five rig systems, component inspection and quizzes. The Meta Quest 3 build places a full-scale rig in your room, with hand tracking and a palm menu. Endorsed by five universities.",
                 [("Mixed-reality demo", "https://www.youtube.com/watch?v=zSYMY_LRfao"),
                  ("reluinteractives.com/…/petsim", "https://reluinteractives.com/solutions/enterprise/education/petsim")]),
                ("VIVaTS", "Ghana National Gas Company",
                 "Operator training and live plant monitoring, built as a working digital twin of national gas infrastructure.",
                 [("Case study", "https://reluinteractives.com/solutions/enterprise/engineering/vivats")]),
                ("Live digital twins", "Industrial",
                 "Interactive 3D replicas of plant and equipment, built from engineering drawings for visualization, monitoring and analysis.", []),
                ("Military VR/AR training", "Soko Aerial Signal Training School",
                 "VR and AR training experiences for new recruits, built in Unity and Blender.", []),
                ("Survey Kit Simulation", "Geomatics",
                 "An interactive 3D guide to surveying instruments such as the total station, for Windows.",
                 [("itch.io", "https://caleb-mantey.itch.io/survey-kit-simulation")]),
            ]),
            ("Games, AR & platform", [
                ("AKOFENA: Blades of the Ancestors", "Free in the browser · TypeScript, three.js",
                 "A fighting game with 19 African legends on 17 home stages, played 1v1 online with rollback netcode over WebRTC or on one screen.",
                 [("akofena.reluspatial.com", "https://akofena.reluspatial.com/")]),
                ("Dark Echoes", "Unity",
                 "A third-person zombie shooter.",
                 [("itch.io", "https://caleb-mantey.itch.io/dark-echoes")]),
                ("Cube Slice", "Android",
                 "A mobile game published on Google Play.",
                 [("Google Play", "https://play.google.com/store/apps/details?id=com.DungaStudios.CubeSlice")]),
                ("AR experiences", "Mobile AR",
                 "Markerless AR placement, brand activations and spatial overlays you see through your phone.", []),
                ("Relu Spatial", "Lead engineer · backend and XR engine",
                 "A browser-native WebXR platform for AI-assisted 3D creation: AR and VR experiences, a desktop editor, and publishing to web, mobile and headsets.",
                 [("reluspatial.com", "https://reluspatial.com/")]),
            ]),
        ],
        "teaching": "Publish a Unity tutorial series on YouTube (@CalebMantey) that builds a third-person bow and arrow system. Playable demos on itch.io.",
        "links_extra": [("itch.io", "https://caleb-mantey.itch.io/")],
        "awards": [
            "2023 NEIP Presidential Pitch, overall winner (Relu Interactives).",
            "2023 Ghana Innovation & Startup Awards, Animation/Gaming Startup Innovation of the Year.",
        ],
        "education": "B.Sc., Geomatic Engineering\nUniversity of Mines and Technology (UMaT), Ghana\nFocus: spatial data, GIS, coordinate systems",
    },
    "software-ai": {
        "summary": "Senior full-stack & AI engineer, Co-Founder/CTO of Relu Interactives, and lead engineer of Relu "
                   "Spatial. I build backend systems, full-stack products, and production AI, from autonomous "
                   "agents and RAG pipelines to LLM workflows that take action, across immersive tech, industrial "
                   "operations, health, workforce, and payments. Strongest backend experience in Ruby on Rails, "
                   "Node.js/NestJS, and Python.",
        "skills": [
            ("Backend & data", "Ruby on Rails, Node.js, NestJS, Python / FastAPI, REST, WebSockets, PostgreSQL, MySQL, Redis"),
            ("Frontend & mobile", "TypeScript, React, Next.js, Angular, Flutter, React Native"),
            ("AI engineering", "LLM APIs (OpenAI, Claude), agents, multi-agent, RAG, LangChain, LangGraph, MCP, evals"),
            ("Delivery", "Docker, AWS, DigitalOcean, GitHub Actions, CI/CD, automated testing, leadership"),
        ],
        "experience": [
            ("Relu Interactives", "Co-Founder & CTO", "Sep 2022 – Present", [
                "Lead engineer of Relu Spatial; built the platform across backend services and its real-time 3D/XR engine, supporting AI-assisted creation, a desktop editor, multi-user sessions, and cross-device publishing.",
                "Built ACTIVA, an operations-intelligence platform for industrial teams with live dashboards, automatic alerts, and a built-in AI assistant.",
                "Set technical direction and lead engineers and designers from product planning through deployment across platform and client work.",
            ]),
            ("Zenjob", "Full-Stack & AI Software Developer", "Jul 2024 – May 2025", [
                "Built AI-powered matching and workflow-automation features for a European staffing platform, integrating LLM tooling into product and operational processes.",
                "Partnered across teams to find automation opportunities and connect new services into existing workflows.",
            ]),
            ("Think-it", "Software / AI Engineer", "Apr 2023 – Jun 2025", [
                "Built and maintained scalable, AI-integrated applications for mission-driven climate- and health-technology partners, with strong tests, docs, and performance work.",
            ]),
            ("Andela / client projects", "Senior Software Engineer", "Sep 2021 – Jan 2024", [
                "Delivered full-stack client projects, backend integrations, and browser-based 3D applications for distributed teams.",
            ]),
            ("Encodev Labs / eGotickets", "Software Engineer", "Sep 2020 – Apr 2023", [
                "Maintained and extended a Ruby on Rails ticketing & payments platform; contributed architecture and mobile engineering to besaCare, a health-access platform.",
            ]),
            ("Dropin", "Senior Software Engineer (Contract)", "Sep 2019 – Aug 2020", [
                "Managed the development team for a ride-hailing app in Ghana and wrote code across the stack: NestJS, WebSockets, PostgreSQL, Docker, and Flutter.",
            ]),
            ("Stanbic Bank Ghana", "Software Developer", "Jun 2019 – Oct 2019", [
                "Implemented frontend and backend features for banking applications (Angular, Java/Spring Boot).",
            ]),
        ],
        "projects": [
            ("Relu Spatial", "Lead engineer; backend + engine for a cross-device 3D/WebXR creation platform."),
            ("ACTIVA", "Industrial operations intelligence with live dashboards, alerts, and a built-in AI assistant."),
            ("Zenjob AI workflows", "LLM-powered matching and operational automation inside a workforce product."),
            ("besaCare", "Healthcare-access platform (appointments, consultations, records); architecture + mobile."),
            ("eGotickets", "Ruby on Rails ticketing & payments platform with features, integrations, and deployment."),
            ("joy_ussd_engine", "Open-source Ruby library for text apps across USSD, WhatsApp, and Telegram."),
        ],
        "teaching": "Publish engineering tutorials (clean architecture, patterns, Unity tools) on GitHub & YouTube.",
        "awards": [
            "2023 NEIP Presidential Pitch, overall winner (Relu Interactives).",
            "2023 Ghana Innovation & Startup Awards, Animation/Gaming Startup Innovation of the Year.",
        ],
        "education": "B.Sc., Geomatic Engineering\nUniversity of Mines and Technology (UMaT), Ghana",
    },
}


def build(kind):
    theme = THEMES[kind]
    data = DATA[kind]
    st = styles(theme)
    acc = theme["accent"]
    path = HERE / f"caleb-mantey-{kind}-cv.pdf"

    doc = BaseDocTemplate(
        str(path), pagesize=A4, title=f"Caleb Mantey · {theme['label']}", author="Caleb Mantey",
        leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
    )
    side_frame = Frame(SIDE_PAD_L, BOT, SIDE_INNER, PAGE_H - TOP - BOT, id="side",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    main_frame = Frame(MAIN_X, BOT, MAIN_W, PAGE_H - TOP - BOT, id="main",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    full_frame = Frame(13 * mm, BOT, PAGE_W - 26 * mm, PAGE_H - BAND - 9 * mm - BOT, id="full",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def paint_first(canvas, _doc):
        canvas.saveState()
        canvas.setFillColor(theme["side"])
        canvas.rect(0, 0, SIDE_W, PAGE_H, stroke=0, fill=1)
        canvas.setFillColor(acc)
        canvas.rect(0, PAGE_H - 6 * mm, SIDE_W, 6 * mm, stroke=0, fill=1)  # accent cap
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - 13 * mm, 8 * mm, "Caleb Mantey · CV")
        canvas.restoreState()

    def paint_later(canvas, _doc):
        canvas.saveState()
        canvas.setFillColor(theme["side"])
        canvas.rect(0, PAGE_H - BAND, PAGE_W, BAND, stroke=0, fill=1)
        canvas.setFillColor(acc)
        canvas.rect(0, PAGE_H - 2.2 * mm, PAGE_W, 2.2 * mm, stroke=0, fill=1)
        canvas.setFont("Helvetica-Bold", 10.5)
        canvas.setFillColor(WHITE)
        canvas.drawString(13 * mm, PAGE_H - BAND + 5.2 * mm, "CALEB MANTEY")
        canvas.setFont("Helvetica-Bold", 7.6)
        canvas.setFillColor(theme["side2"])
        canvas.drawRightString(PAGE_W - 13 * mm, PAGE_H - BAND + 5.4 * mm, theme["label"])
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - 13 * mm, 8 * mm, "Caleb Mantey · CV")
        canvas.restoreState()

    doc.addPageTemplates([
        PageTemplate(id="first", frames=[side_frame, main_frame], onPage=paint_first),
        PageTemplate(id="later", frames=[full_frame], onPage=paint_later),
    ])

    def P(text, s):
        return Paragraph(text, st[s])

    def s_head(label):
        return P(label.upper(), "s_head")

    def m_head(label):
        return [P(label.upper(), "m_head"),
                HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=1, spaceAfter=5)]

    story = []

    # ---- sidebar ----
    story += [P("CALEB", "name"), P("MANTEY", "name"), P(theme["label"], "role")]
    story += [s_head("Contact")]
    for c in CONTACT:
        story.append(P(escape(c), "s_body"))
    story += [s_head("Core skills")]
    for label, value in data["skills"]:
        story.append(P(escape(label), "s_lbl"))
        story.append(P(escape(value), "s_val"))
    story += [s_head("Education")]
    for line in data["education"].split("\n"):
        story.append(P(escape(line), "s_val" if line == data["education"].split("\n")[0] else "s_dim"))
    story += [s_head("Recognition")]
    for a in data["awards"]:
        story.append(P("• " + escape(a), "s_dim"))
    story += [s_head("Links")]
    link_rows = list(LINKS) + list(data.get("links_extra", []))
    for label, url in link_rows:
        story.append(P(f'<link href="{url}" color="#b7bdff">{escape(label)}</link>', "s_val"))
    story += [s_head("Open source & teaching"), P(escape(data["teaching"]), "s_dim")]

    story.append(FrameBreak())
    story.append(NextPageTemplate("later"))

    # ---- main ----
    story += m_head("Profile") + [P(escape(data["summary"]), "body")]

    story += m_head("Experience")
    for company, role, dates, bullets in data["experience"]:
        block = [P(f"{escape(company)} &nbsp;·&nbsp; {escape(role)}", "job"), P(escape(dates), "meta")]
        block += [P("•&nbsp; " + escape(b), "bullet") for b in bullets]
        story.append(KeepTogether(block))

    story += m_head(data.get("projects_title", "Selected projects"))
    if "project_groups" in data:
        acc_hex = acc.hexval().replace("0x", "#")
        for group, items in data["project_groups"]:
            story.append(P(escape(group).upper(), "p_group"))
            for name, context, desc, links in items:
                link_html = " · ".join(
                    f'<link href="{escape(u)}" color="{acc_hex}"><u>{escape(lbl)}</u></link>' for lbl, u in links)
                story.append(P(
                    f"<b>{escape(name)}</b> &nbsp;<font color='#5a6478'>{escape(context)}</font><br/>"
                    f"{escape(desc)}" + (f" {link_html}" if links else ""), "proj2"))
    else:
        for name, desc in data["projects"]:
            story.append(P(f"<b>{escape(name)}</b> &nbsp;·&nbsp; {escape(desc)}", "proj"))

    doc.build(story)
    print("built", path.name)


if __name__ == "__main__":
    for kind in DATA:
        build(kind)
