#!/usr/bin/env python3
import os, re, json, collections, sys
from pathlib import Path

# --- stopword / noise blacklist ---
STOPWORDS = set("""
a about above across after again against all almost along already also although am among an and another any anybody anyone anything anyway anywhere are aren't around as at back be became because been before being below beneath beside besides between beyond both but by can cannot can't come comes could couldn't did didn't do does doesn't doing don't down during each either else elsewhere end enough even ever every everybody everyone everything everywhere few find for found from further get getting give gives go going gone got had hadn't has hasn't have haven't having he he'd he'll he's her here hers herself him himself his how however i i'd i'll i'm i've if in inside instead into is isn't it it's itself keep kept know known last least let let's like likely long look looks made make makes many may maybe me might mine more most mostly much must my myself near need neither never next no nobody none noone nor not nothing now nowhere of off often on once one only onto or other others our ours ourselves out over own please put quite rather really same say says see seemed seeming seems seen shall she she'd she'll she's should shouldn't since so some somebody someone something sometimes somewhere still such sure take taken taking than that that's the their theirs them themselves then there there's these they they'd they'll they're they've thing things think this those though through throughout till time to too took toward towards try trying under until up upon us used uses using usually very want wants was wasn't way we we'd well we're weren't we've what what's when when's where where's whether which while who who's whom whose why why's will with within without won't would wouldn't yes yet you you'd you'll you're you've your yours yourself yourselves

um uh like you know actually basically sort kind mean see well so right okay anyways look listen believe frankly literally just pretty much perhaps guess think you know what at the end of the day to be honest to tell you the truth in a sense if you will you know what i mean at all whatsoever stuff lets say in other words suppose definitely certainly surely absolutely totally completely utterly essentially fundamentally practically virtually nearly almost about around approximately roughly someway somehow sometime sometimes occasionally often frequently regularly usually typically generally mainly mostly largely particularly especially specifically expressly explicitly precisely exactly merely simply only solely probably maybe possibly seemingly apparently ostensibly evidently presumably assumably likely quite rather somewhat more or less to some extent to an extent up to a point in part partly partially not entirely not totally not wholly not fully by and large on the whole all in all for the most part in general as a rule generally speaking

code codes coding function script scripts run running execute executed command commands bash termux system sys kernel text txt file files data dataset datasets json csv html com name path paths dir directory directories output input variable variables param parameter params config terminal shell linux python version install clone repo github git env venv virtual import print type class object value values key keys line lines start step end return def while for if else elif true false null none read write open close append log error debug warn warning result results output process processes model models metadata content token tokens url urls https http index indices source sources ref refs reference references citation citations default async complete completion parts search channel request response role author recipient message messages absolute finished success successfully update create parent children weight slug timestamp voice audio image gizmo mode user assistant attribution feel real nyou bbb details finish

isn wasn aren wasn’t isn’t didn doesn’t don’t didn’t wasn wasn’t shouldn shouldn’t couldn couldn’t hadn hadn’t hasn hasn’t haven haven’t weren weren’t

it there this that those these here where when what who which someone anyone everyone everything something nothing anything nobody none whoever whatever whichever wherever whenever somehow sometime somewhere thereby therein therefore thus hence accordingly consequently moreover furthermore besides meanwhile overall otherwise however nevertheless nonetheless

action actions decision decisions creation situation situations information communication explanation observation determination realization expectation understanding consideration organization implementation motivation permission assumption conclusion condition position possession relation connection expression discussion intention function operation participation perception suggestion recognition transformation construction description combination selection preparation interpretation attention affection reflection projection protection prediction evaluation application reaction invitation instruction education repetition presentation production limitation indication adaptation association expression resolution tension extension submission transmission omission emission opposition depression progression suppression obsession possession direction perfection collection correction infection suggestion intention attention decision action motion notion emotion sensation creation operation function communication regulation relation combination determination contribution production perception description competition construction destruction observation collection connection translation condition reaction solution resolution conclusion expression discussion profession succession aggression suggestion permission protection completion opposition depression ambition admission omission recognition definition perception repetition tradition education attention information association organization situation condition relation position expression addition selection connection operation invitation election perception affection reflection suggestion intention attention possession presentation representation temptation communication application combination education relation decision creation situation action motion notion emotion reflection perception understanding development establishment improvement arrangement agreement movement requirement involvement management statement payment treatment enjoyment attachment assessment judgment announcement replacement adjustment commitment engagement containment employment acknowledgment argument nourishment environment accomplishment achievement investment development refinement punishment amazement encouragement endowment alignment assignment confinement refinement enlightenment acknowledgment embarrassment enhancement
each_and_every first_and_foremost end_result final_outcome basic_fundamentals close_proximity general_public true_fact unexpected_surprise free_gift personal_opinion future_plan past_history advance_warning mutual_cooperation new_innovation completely_finished repeat_again added_bonus small_size completely_unique return_back reason_why

moment yeah yes no people emotional feels feeling alright felt message script ask said part some never always got make too back all let don there their they're

quot turn status gpt stop title chatgpt nand asset www video utm date pointer amp snippet pub idx nthat were doesn atl hidden dfw nso nbut nit groups gen trigger conversation dictation queries attributions transcription prompt size ufffd nhe use nif reason reasoning matched dafb safe alt high means box nbecause
""".split())

# --- text normalization ---
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z'\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --- tokenization & counting ---
def count_words_in_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        try:
            data = json.load(f)
            if isinstance(data, dict) and "mapping" in data:
                text = json.dumps(data)
            elif isinstance(data, list):
                text = json.dumps(data)
            else:
                text = f.read()
        except Exception:
            f.seek(0)
            text = f.read()
    text = normalize(text)
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    return collections.Counter(words)

# --- main ---
def main():
    if len(sys.argv) < 2:
        print("Usage: python src/top_words.py <input_dir>")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    all_counts = collections.Counter()

    for path in input_dir.rglob("*.json"):
        counts = count_words_in_file(path)
        all_counts.update(counts)

    print("Top 50 surviving words:")
    for word, freq in all_counts.most_common(50):
        print(f"{word:20s} {freq}")

if __name__ == "__main__":
    main()
