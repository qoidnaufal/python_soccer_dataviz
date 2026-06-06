use std::{collections::{HashMap, HashSet}, fs::File, io::Write};
use serde::{Serialize, Deserialize};

const ACADEMY_PRODUCT_DATA: &str = include_str!("../../youth_data/2526/youth_data.csv");
const MOP: &str = include_str!("../../youth_data/2526/mop.csv");

#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Eq, Hash)]
enum ClubName {
    #[serde(rename(serialize = "PSIS Semarang"), alias = "PSIS SEMARANG", alias = "PSIS Semarang", alias = "PSIS")]
    PSISSemarang,
    #[serde(rename(serialize = "PSS Sleman"), alias = "PSS SLEMAN", alias = "PSS Sleman", alias = "PSS")]
    PSSSleman,
    #[serde(rename(serialize = "Persib Bandung"), alias = "PERSIB BANDUNG", alias = "Persib Bandung", alias = "Persib")]
    PersibBandung,
    #[serde(rename(serialize = "Barito Putera"), alias = "PS BARITO PUTERA", alias = "PS Barito Putera", alias = "Barito Putera")]
    BaritoPutera,
    #[serde(rename(serialize = "Persik Kediri"), alias = "PERSIK KEDIRI", alias = "Persik Kediri", alias = "Persik")]
    PersikKediri,
    #[serde(rename(serialize = "Dewa United"), alias = "DEWA UNITED BANTEN FC", alias = "Dewa United")]
    DewaUnited,
    #[serde(rename(serialize = "Persebaya Surabaya"), alias = "PERSEBAYA SURABAYA", alias = "Persebaya Surabaya", alias = "Persebaya")]
    PersebayaSurabaya,
    #[serde(rename(serialize = "Persija Jakarta"), alias = "PERSIJA JAKARTA", alias = "Persija Jakarta", alias = "Persija")]
    PersijaJakarta,
    #[serde(rename(serialize = "Arema"), alias = "AREMA FC", alias = "Arema FC", alias = "Arema")]
    Arema,
    #[serde(rename(serialize = "PSM Makassar"), alias = "PSM MAKASSAR", alias = "PSM Makassar")]
    PSMMakassar,
    #[serde(rename(serialize = "Bali United"), alias = "BALI UNITED FC", alias = "Bali United")]
    BaliUnited,
    #[serde(rename(serialize = "Persita Tangerang"), alias = "PERSITA", alias = "Persita Tangerang", alias = "Persita")]
    PersitaTangerang,
    #[serde(rename(serialize = "Borneo FC"), alias = "BORNEO FC SAMARINDA", alias = "Borneo FC")]
    BorneoFC,
    #[serde(rename(serialize = "Semen Padang"), alias = "SEMEN PADANG FC", alias = "Semen Padang")]
    SemenPadang,
    #[serde(rename(serialize = "Madura United"), alias = "MADURA UNITED FC", alias = "Madura United")]
    MaduraUnited,
    #[serde(rename(serialize = "PSBS Biak"), alias = "PSBS BIAK", alias = "PSBS Biak", alias = "PSBS")]
    PSBSBiak,
    #[serde(rename(serialize = "Persis Solo"), alias = "PERSIS SOLO", alias = "Persis Solo", alias = "Persis")]
    PersisSolo,
    #[serde(rename(serialize = "Malut United"), alias = "MALUT UNITED FC", alias = "Malut United FC", alias = "Malut United")]
    MalutUnited,
    #[serde(rename(serialize = "Persijap Jepara"), alias = "PERSIJAP JEPARA", alias = "Persijap Jepara", alias = "Persijap")]
    Persijap,
    #[serde(rename(serialize = "PSIM Yogyakarta"), alias = "PSIM YOGYAKARTA", alias = "PSIM Yogyakarta", alias = "PSIM")]
    PSIM,
    #[serde(rename(serialize = "Bhayangkara Presisi Lampung FC"), alias = "BHAYANGKARA PRESISI LAMPUNG FC", alias = "Bhayangkara Presisi Lampung FC", alias = "Bhayangkara")]
    Bhayangkara,
    #[serde(rename(serialize = "Garudayaksa"), alias = "GARUDAYAKSA FC", alias = "Garudayaksa FC", alias = "Garudayaksa")]
    Garudayaksa,
    #[serde(rename(serialize = "Adhyaksa FC Banten"), alias = "ADHYAKSA FC BANTEN", alias = "Adhyaksa FC Banten", alias = "Adhyaksa")]
    Adhyaksa,
    #[serde(rename(serialize = "Persipura"), alias = "PERSIPURA JAYAPURA", alias = "Persipura Jayapura", alias = "Persipura")]
    Persipura,
    #[serde(rename(serialize = "Persiraja Banda Aceh"), alias = "PERSIRAJA BANDA ACEH", alias = "Persiraja Banda Aceh", alias = "Persiraja")]
    Persiraja,
    #[serde(rename(serialize = "Persipal FC"), alias = "PERSIPAL FC", alias = "Persipal FC", alias = "Persipal")]
    Persipal,
    #[serde(rename(serialize = "Deltras FC"), alias = "DELTRAS FC", alias = "Deltras FC", alias = "Deltras")]
    Deltras,
    #[serde(rename(serialize = "FC Bekasi City"), alias = "FC BEKASI CITY", alias = "FC Bekasi City", alias = "Bekasi FC")]
    FCBekasiCity,
    #[serde(rename(serialize = "Kendal Tornado FC"), alias = "KENDAL TORNADO FC", alias = "Kendal Tornado FC", alias = "Kendal Tornado")]
    KendalTornadoFC,
    #[serde(rename(serialize = "Persekat Tegal"), alias = "PERSEKAT TEGAL", alias = "Persekat Tegal", alias = "Persekat")]
    Persekat,
    #[serde(rename(serialize = "Persela Lamongan"), alias = "PERSELA LAMONGAN", alias = "Persela Lamongan", alias = "Persela")]
    Persela,
    #[serde(rename(serialize = "Persiba Balikpapan"), alias = "PERSIBA BALIKPAPAN", alias = "Persiba Balikapapan", alias = "Persiba")]
    PersibaBalikpapan,
    #[serde(rename(serialize = "Persikad Depok"), alias = "PERSIKAD", alias = "Persikad Depok", alias = "Persikad")]
    Persikad,
    #[serde(rename(serialize = "Persiku Kudus"), alias = "PERSIKU KUDUS", alias = "Persiku Kudus", alias = "Persiku")]
    Persiku,
    #[serde(rename(serialize = "PSMS Medan"), alias = "PSMS MEDAN", alias = "PSMS Medan", alias = "PSMS")]
    PSMS,
    #[serde(rename(serialize = "PSPS Pekanbaru"), alias = "PSPS PEKANBARU", alias = "PSPS Pekanbaru", alias = "PSPS")]
    PSPS,
    #[serde(rename(serialize = "Sriwijaya FC"), alias = "SRIWIJAYA FC", alias = "Sriwijaya FC", alias = "Sriwijaya")]
    SriwijayaFC,
    #[serde(rename(serialize = "Sumsel United"), alias = "SUMSEL UNITED", alias = "Sumsel United", alias = "Sumsel")]
    SumselUnited,
}

impl std::fmt::Display for ClubName {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let s = match self {
            Self::PSISSemarang => "PSIS Semarang",
            Self::PSSSleman => "PSS Sleman",
            Self::PersibBandung => "Persib Bandung",
            Self::BaritoPutera => "Barito Putera",
            Self::PersikKediri => "Persik Kediri",
            Self::DewaUnited => "Dewa United",
            Self::PersebayaSurabaya => "Persebaya Surabaya",
            Self::PersijaJakarta => "Persija Jakarta",
            Self::Arema => "Arema",
            Self::PSMMakassar => "PSM Makassar",
            Self::BaliUnited => "Bali United",
            Self::PersitaTangerang => "Persita Tangerang",
            Self::BorneoFC => "Borneo FC",
            Self::SemenPadang => "Semen Padang",
            Self::MaduraUnited => "Madura United",
            Self::PSBSBiak => "PSBS Biak",
            Self::PersisSolo => "Persis Solo",
            Self::MalutUnited => "Malut United",
            Self::Persijap => "Persijap Jepara",
            Self::PSIM => "PSIM Yogyakarta",
            Self::Bhayangkara => "Bhayangkara Presisi Lampung FC",
            Self::Garudayaksa => "Garudayaksa",
            Self::Adhyaksa => "Adhyaksa Banten FC",
            Self::Persipura => "Persipura Jayapura",
            Self::Persiraja => "Persiraja Banda Aceh",
            Self::Persipal => "Persipal FC",
            Self::Deltras => "Deltras FC",
            Self::FCBekasiCity => "FC Bekasi City",
            Self::KendalTornadoFC => "Kendal Tornado",
            Self::Persekat => "Persekat Tegal",
            Self::Persela => "Persela Lamongan",
            Self::PersibaBalikpapan => "Persiba Balikpapan",
            Self::Persikad => "Persikad Depok",
            Self::Persiku => "Persiku Kudus",
            Self::PSMS => "PSMS Medan",
            Self::PSPS => "PSPS Pekanbaru",
            Self::SriwijayaFC => "Sriwijaya FC",
            Self::SumselUnited => "Sumsel United",
        };
        write!(f, "{s}")
    }
}

impl core::fmt::Debug for ClubName {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

#[derive(Debug, Serialize, Deserialize, Clone, Copy)]
enum Position {
    GK,
    #[serde(alias = "DF", alias = "CB", alias = "FB")]
    DF,
    MF,
    WG,
    #[serde(alias = "CF")]
    FW,
    #[serde(alias = "-", alias = "")]
    NP,
}

#[derive(Debug, Serialize, Deserialize, PartialEq, Eq, Clone, Copy)]
enum CompetitionTier {
    #[serde(rename(serialize = "Liga 1"), alias = "BRI Liga 1", alias = "Liga 1", alias = "BRI SUPER LEAGUE 2025-26")]
    BRILiga1,
    #[serde(rename(serialize = "Liga 2"), alias = "Pegadaian Liga 2", alias = "Liga 2", alias = "PEGADAIAN CHAMPIONSHIP 2025-26")]
    PegadaianLiga2
}

#[derive(Debug, Serialize, Deserialize)]
struct Row {
    #[serde(alias = "Club now", alias = "Club Now", alias = "Team")]
    club_now: ClubName,
    #[serde(rename(deserialize = "Name"))]
    name: String,
    #[serde(alias = "DOB", alias = "DoB")]
    dob: String,
    #[serde(rename(deserialize = "Pos"))]
    pos: Position,
    #[serde(alias = "Minutes", alias = "MoP", alias = "MOP")]
    minutes: f32,
    #[serde(rename(deserialize = "Games"))]
    games: f32,
    #[serde(alias = "Youth club", alias = "Youth Club")]
    youth_club: ClubName,
    #[serde(alias = "Club tier", alias = "Club Competition")]
    competition: CompetitionTier,
    #[serde(alias = "Youth club Tier", alias = "Youth club tier", alias = "Youth Club Competition")]
    y_competition: CompetitionTier,
}

#[derive(Debug)]
struct AcademyProduct {
    club_now: ClubName,
    dob: String,
    pos: Position,
    minutes: f32,
    games: f32,
    youth_club: HashSet<ClubName>,
    competition: CompetitionTier,
    y_competition: CompetitionTier,
}

#[derive(Debug, Serialize)]
struct Player {
    #[serde(rename(serialize = "Name"))]
    name: String,
    #[serde(rename(serialize = "DoB"))]
    dob: String,
    #[serde(rename(serialize = "Pos"))]
    pos: Position,
    #[serde(rename(serialize = "Minutes"))]
    minutes: f32,
    #[serde(rename(serialize = "Games"))]
    games: f32,
    #[serde(rename(serialize = "Club Now"))]
    club_now: ClubName,
    #[serde(rename(serialize = "Club Competition"))]
    competition: CompetitionTier,
    #[serde(rename(serialize = "Youth Club Competition"))]
    y_competition: CompetitionTier,
    #[serde(rename(serialize = "Youth Clubs"))]
    youth_clubs: u8,
}

#[derive(Debug, Serialize)]
struct YouthClub {
    #[serde(rename(serialize = "Club Name"))]
    club_name: ClubName,

    #[serde(rename(serialize = "Registered"))]
    players_count: usize,
    #[serde(rename(serialize = "in Liga 1"))]
    in_l1: usize,
    #[serde(rename(serialize = "in Club"))]
    in_club: usize,
    #[serde(rename(serialize = "in Other Liga 1"))]
    in_other_l1: usize,
    #[serde(rename(serialize = "in Liga 2"))]
    in_l2: usize,

    #[serde(rename(serialize = "Players with Minutes"))]
    players_with_minutes: usize,

    #[serde(rename(serialize = "Played in Liga 1"))]
    with_minutes_in_l1: usize,
    #[serde(rename(serialize = "Played in Club"))]
    with_minutes_in_club: usize,
    #[serde(rename(serialize = "Played in Other Liga 1"))]
    with_minutes_in_other_l1: usize,

    #[serde(rename(serialize = "Played in Liga 2"))]
    with_minutes_in_l2: usize,
    #[serde(rename(serialize = "Played in Liga 2 Regular Teams"))]
    with_minutes_in_l2_regular: usize,
    #[serde(rename(serialize = "Played in Liga 2 Playoff Teams"))]
    with_minutes_in_l2_playoff: usize,
    #[serde(rename(serialize = "Played in Liga 2 Final Teams"))]
    with_minutes_in_l2_final: usize,

    #[serde(rename(serialize = "Adj Total Games"))]
    adj_games: u32,
    #[serde(rename(serialize = "Adj Total Minutes"))]
    adj_minutes: u32,

    #[serde(rename(serialize = "Adj Minutes in Liga 1"))]
    adj_minutes_in_l1: u32,
    #[serde(rename(serialize = "Adj Minutes in Club"))]
    adj_minutes_in_club: u32,
    #[serde(rename(serialize = "Adj Minutes in Other Liga 1"))]
    adj_minutes_in_other_l1: u32,

    #[serde(rename(serialize = "Adj Minutes in Liga 2"))]
    adj_minutes_in_l2: u32,
    #[serde(rename(serialize = "Adj Minutes in Liga 2 Regular Teams"))]
    adj_minutes_in_l2_regular: u32,
    #[serde(rename(serialize = "Adj Minutes in Liga 2 Playoff Teams"))]
    adj_minutes_in_l2_playoff: u32,
    #[serde(rename(serialize = "Adj Minutes in Liga 2 Final Teams"))]
    adj_minutes_in_l2_final: u32,

    #[serde(rename(serialize = "Total Minutes"))]
    total_minutes: u32,
    #[serde(rename(serialize = "Total Games"))]
    total_games: u32,

    #[serde(rename(serialize = "Minutes in Liga 1"))]
    minutes_in_l1: u32,
    #[serde(rename(serialize = "Minutes in Club"))]
    minutes_in_club: u32,
    #[serde(rename(serialize = "Minutes in Other Liga 1"))]
    minutes_in_other_l1: u32,

    #[serde(rename(serialize = "Minutes in Liga 2"))]
    minutes_in_l2: u32,
    #[serde(rename(serialize = "Minutes in Liga 2 Regular"))]
    minutes_in_l2_regular: u32,
    #[serde(rename(serialize = "Minutes in Liga 2 Playoff"))]
    minutes_in_l2_playoff: u32,
    #[serde(rename(serialize = "Minutes in Liga 2 Final"))]
    minutes_in_l2_final: u32,

    #[serde(skip)]
    players: Vec<Player>,
}

const PLAYOFF_TEAMS: [ClubName; 4] = [
    ClubName::Adhyaksa,
    ClubName::Persipura,
    ClubName::PersibaBalikpapan,
    ClubName::Persekat
];

const FINAL_TEAMS: [ClubName; 2] = [
    ClubName::Garudayaksa,
    ClubName::PSSSleman,
];

fn get_ap_data<F, const N: usize>(
    query: &Query<N>,
    player_data: HashMap<String, AcademyProduct>,
    f: F
) -> HashMap<ClubName, YouthClub>
where
    F: FnMut(&(&String, &AcademyProduct)) -> bool,
{
    let mut youth_clubs: HashMap<ClubName, YouthClub> = HashMap::new();

    player_data
        .iter()
        .filter(f)
        .for_each(|(name, data)| {
            let len = data.youth_club.len() as f32;
            let player_minutes = data.minutes.round() as u32;
            let player_games = data.games.round() as u32;
            let adj_minutes = (data.minutes / len).round() as u32;
            let adj_games = (data.games / len).round() as u32;
            let with_minute = data.minutes > 0.;
            let played = with_minute as usize;

            let l1 = matches!(data.competition, CompetitionTier::BRILiga1);
            let l2 = matches!(data.competition, CompetitionTier::PegadaianLiga2);
            let l2_playoff = PLAYOFF_TEAMS.contains(&data.club_now);
            let l2_final = FINAL_TEAMS.contains(&data.club_now);
            let l2_regular = !l2_playoff && !l2_final;

            for club in &data.youth_club {
                youth_clubs
                    .entry(*club)
                    .and_modify(|yc| {
                        yc.adj_minutes += adj_minutes;
                        yc.adj_games += adj_games;
                        yc.players_count += 1;
                        yc.players_with_minutes += played;
                        yc.total_minutes += player_minutes;
                        yc.total_games += player_games;

                        match data.competition {
                            CompetitionTier::BRILiga1 => {
                                yc.in_l1 += 1;
                                yc.with_minutes_in_l1 += played;
                                yc.minutes_in_l1 += player_minutes;
                                yc.adj_minutes_in_l1 += adj_minutes;

                                if *club == data.club_now {
                                    yc.in_club += 1;
                                    yc.with_minutes_in_club += played;
                                    yc.minutes_in_club += player_minutes;
                                    yc.adj_minutes_in_club += adj_minutes;
                                }
                                if *club != data.club_now {
                                    yc.in_other_l1 += 1;
                                    yc.with_minutes_in_other_l1 += played;
                                    yc.minutes_in_other_l1 += player_minutes;
                                    yc.adj_minutes_in_other_l1 += adj_minutes;
                                }
                            },
                            CompetitionTier::PegadaianLiga2 => {
                                yc.in_l2 += 1;
                                yc.with_minutes_in_l2 += played;
                                yc.minutes_in_l2 += player_minutes;
                                yc.adj_minutes_in_l2 += adj_minutes;

                                if l2_playoff {
                                    yc.with_minutes_in_l2_playoff += played;
                                    yc.minutes_in_l2_playoff += player_minutes;
                                    yc.adj_minutes_in_l2_playoff += adj_minutes;
                                }
                                if l2_final {
                                    yc.with_minutes_in_l2_final += played;
                                    yc.minutes_in_l2_final += player_minutes;
                                    yc.adj_minutes_in_l2_final += adj_minutes;
                                }
                                if l2_regular {
                                    yc.with_minutes_in_l2_regular += played;
                                    yc.minutes_in_l2_regular += player_minutes;
                                    yc.adj_minutes_in_l2_regular += adj_minutes;
                                }
                            },
                        }

                        yc.players.push(Player {
                            name: name.clone(),
                            dob: data.dob.clone(),
                            minutes: data.minutes,
                            games: data.games,
                            pos: data.pos,
                            club_now: data.club_now,
                            competition: data.competition,
                            y_competition: data.y_competition,
                            youth_clubs: len as u8,
                        });
                    })
                    .or_insert(YouthClub {
                        club_name: *club,

                        players_count: 1,
                        in_l1: l1 as usize,
                        in_club: (*club == data.club_now) as usize,
                        in_other_l1: (l1 && *club != data.club_now) as usize,
                        in_l2: l2 as usize,

                        players_with_minutes: played,
                        with_minutes_in_l1: (with_minute && l1) as usize,
                        with_minutes_in_club: (with_minute && data.club_now == *club) as usize,
                        with_minutes_in_other_l1: (with_minute && (l1 && data.club_now == *club)) as usize,

                        with_minutes_in_l2: (with_minute && l2) as usize,
                        with_minutes_in_l2_regular: (with_minute && (l2 && l2_regular)) as usize,
                        with_minutes_in_l2_playoff: (with_minute && (l2 && l2_playoff)) as usize,
                        with_minutes_in_l2_final: (with_minute && (l2 && l2_final)) as usize,

                        adj_games,
                        adj_minutes,

                        adj_minutes_in_l1: adj_minutes * (l1 as u32),
                        adj_minutes_in_club: adj_minutes * ((l1 && *club == data.club_now) as u32),
                        adj_minutes_in_other_l1: adj_minutes * ((l1 && *club != data.club_now) as u32),

                        adj_minutes_in_l2: adj_minutes * (l2 as u32),
                        adj_minutes_in_l2_regular: adj_minutes * ((l2 && l2_regular) as u32),
                        adj_minutes_in_l2_playoff: adj_minutes * ((l2 && l2_playoff) as u32),
                        adj_minutes_in_l2_final: adj_minutes * ((l2 && l2_final) as u32),

                        total_minutes: player_minutes,
                        total_games: player_games,

                        minutes_in_l1: player_minutes * (l1 as u32),
                        minutes_in_club: player_minutes * ((l1 && *club == data.club_now) as u32),
                        minutes_in_other_l1: player_minutes * ((l1 && *club != data.club_now) as u32),

                        minutes_in_l2: player_minutes * (l2 as u32),
                        minutes_in_l2_regular: player_minutes * ((l2 && l2_regular) as u32),
                        minutes_in_l2_playoff: player_minutes * ((l2 && l2_playoff) as u32),
                        minutes_in_l2_final: player_minutes * ((l2 && l2_final) as u32),

                        players: {
                            vec![Player {
                                name: name.clone(),
                                dob: data.dob.clone(),
                                minutes: data.minutes,
                                games: data.games,
                                pos: data.pos,
                                club_now: data.club_now.clone(),
                                competition: data.competition,
                                y_competition: data.y_competition,
                                youth_clubs: len as u8,
                            }]
                        },
                    });
            }
        });

    let not_exist = query.clubs.iter()
        .filter(|c| !youth_clubs.contains_key(c))
        .copied()
        .collect::<Vec<_>>();

    not_exist.iter().for_each(|c| {
        youth_clubs.insert(*c, YouthClub {
            club_name: *c,

            players_count: 0,
            in_l1: 0,
            in_club: 0,
            in_other_l1: 0,
            in_l2: 0,

            players_with_minutes: 0,
            with_minutes_in_l1: 0,
            with_minutes_in_club: 0,
            with_minutes_in_other_l1: 0,

            with_minutes_in_l2: 0,
            with_minutes_in_l2_regular: 0,
            with_minutes_in_l2_playoff: 0,
            with_minutes_in_l2_final: 0,

            adj_games: 0,
            adj_minutes: 0,

            adj_minutes_in_l1: 0,
            adj_minutes_in_club: 0,
            adj_minutes_in_other_l1: 0,

            adj_minutes_in_l2: 0,
            adj_minutes_in_l2_regular: 0,
            adj_minutes_in_l2_playoff: 0,
            adj_minutes_in_l2_final: 0,

            total_minutes: 0,
            total_games: 0,

            minutes_in_l1: 0,
            minutes_in_club: 0,
            minutes_in_other_l1: 0,

            minutes_in_l2: 0,
            minutes_in_l2_regular: 0,
            minutes_in_l2_playoff: 0,
            minutes_in_l2_final: 0,

            players: vec![],
        });
    });

    youth_clubs
}

fn parse_dob(s: &str) -> String {
    if s.contains('/') {
        let mut iter = s.split('/');
        let Some(date) = iter.nth(0) else { return "_".to_string() };
        let Some(month) = iter.nth(1) else { return "_".to_string() };
        let Some(year) = iter.nth(2) else { return "-".to_string() };

        let Ok(year) = year.parse::<u32>() else { return "-".to_string() };

        let year = if year < 30 {
            2000 + year
        } else {
            1900 + year
        };
        return format!("{year}-{month}-{date}")
    }

    return s.to_string()
}

fn academy_product<const N: usize>(query: &Query<N>) -> Result<(), Box<dyn std::error::Error>> {
    let mut df = csv::Reader::from_reader(ACADEMY_PRODUCT_DATA.as_bytes());
    let mut iter = df.deserialize();
    let mut player_data: HashMap<String, AcademyProduct> = HashMap::new();

    while let Some(record) = iter.next() {
        let row: Row = record?;
        player_data.entry(row.name)
            .and_modify(|data| { data.youth_club.insert(row.youth_club); })
            .or_insert(AcademyProduct {
                club_now: row.club_now,
                dob: parse_dob(&row.dob),
                pos: row.pos,
                minutes: row.minutes,
                games: row.games,
                youth_club: {
                    let mut h = HashSet::new();
                    h.insert(row.youth_club);
                    h
                },
                competition: row.competition,
                y_competition: row.y_competition,
            });
    }

    let youth_clubs = get_ap_data(query, player_data, |(_, data)| {
        data.competition == CompetitionTier::BRILiga1
        || data.competition == CompetitionTier::PegadaianLiga2
    });

    let mut writer = csv::Writer::from_writer(vec![]);
    youth_clubs.iter().try_for_each(|(_, data)| {
        writer.serialize(data)?;

        Ok::<(), Box<dyn std::error::Error>>(())
    })?;
    let data = String::from_utf8(writer.into_inner()?)?;

    let mut file = File::create("./data/academy_product.csv")?;
    file.write_all(data.as_bytes())?;

    Ok(())
}

#[derive(Debug, Serialize)]
struct YouthMinutes {
    #[serde(rename(serialize = "Team"))]
    club_name: ClubName,
    #[serde(rename(serialize = "Competition"))]
    competition: CompetitionTier,
    #[serde(rename(serialize = "Players with Minutes"))]
    players_with_minutes: usize,
    #[serde(rename(serialize = "Total Minutes"))]
    total_minutes: u32,
    #[serde(rename(serialize = ">= 900"))]
    nine_hundred: u8,
}

#[derive(Debug, Deserialize)]
struct MoP {
    #[serde(rename(deserialize = "Name"))]
    name: String,
    #[serde(alias = "Club now", alias = "Club Now", alias = "Team")]
    team: ClubName,
    #[serde(alias = "Minutes", alias = "MoP", alias = "MOP")]
    minutes: u32,
    #[serde(alias = "Age")]
    age: u8,
    #[serde(alias = "DOB", alias = "DoB")]
    _dob: String,
    #[serde(rename(deserialize = "Nationality"))]
    nationality: String,
    #[serde(rename(deserialize = "Competition"))]
    competition: CompetitionTier,
}

#[derive(Debug, Serialize)]
struct AllYouthMinutes {
    #[serde(rename(serialize = "Name"))]
    name: String,
    #[serde(rename(serialize = "Team"))]
    club_name: ClubName,
    #[serde(rename(serialize = "Competition"))]
    competition: CompetitionTier,
    #[serde(rename(serialize = "Minutes"))]
    minutes: u32,
}

#[derive(Debug, Serialize)]
struct NineHundred {
    #[serde(rename(serialize = "Name"))]
    name: String,
    #[serde(rename(serialize = "Team"))]
    club_name: ClubName,
    #[serde(rename(serialize = "Competition"))]
    competition: CompetitionTier,
    #[serde(rename(serialize = "Minutes"))]
    minutes: u32,
}

fn parse_name(s: &str) -> String {
    let mut name = String::new();
    let mut iter = s.split_whitespace();
    while let Some(n) = iter.next() {
        let mut c = n.chars();
        let first = c.nth(0).unwrap();
        for u in first.to_uppercase() {
            name.push(u);
        }
        while let Some(rem) = c.next() {
            for l in rem.to_lowercase() {
                name.push(l);
            }
        }
        name.push_str(" ");
    }
    name.trim_ascii_end().to_string()
}

fn youth_contribution() -> Result<(), Box<dyn std::error::Error>> {
    let mut club_data: HashMap<ClubName, YouthMinutes> = HashMap::new();
    let mut nine_hundred_players = vec![];
    let mut all_youth_minutes = vec![];

    let mut mop = csv::Reader::from_reader(MOP.as_bytes());
    let mut iter = mop.deserialize();

    while let Some(record) = iter.next() {
        let mop: MoP = record?;

        if mop.nationality == "Indonesia" && mop.age <= 23 {
            let name = parse_name(&mop.name);
            all_youth_minutes.push(AllYouthMinutes {
                name: name.clone(),
                club_name: mop.team,
                competition: mop.competition,
                minutes: mop.minutes,
            });
            if mop.minutes >= 900 {
                nine_hundred_players.push(NineHundred {
                    name,
                    club_name: mop.team,
                    competition: mop.competition,
                    minutes: mop.minutes,
                });
            }
            club_data.entry(mop.team)
                .and_modify(|youth| {
                    youth.players_with_minutes += (mop.minutes > 0) as usize;
                    youth.total_minutes += mop.minutes;
                    youth.nine_hundred += (mop.minutes >= 900) as u8;
                })
                .or_insert(YouthMinutes {
                    club_name: mop.team,
                    competition: mop.competition,
                    players_with_minutes: (mop.minutes > 0) as usize,
                    total_minutes: mop.minutes,
                    nine_hundred: (mop.minutes >= 900) as u8,
                });
        }

        {
            let mut writer = csv::Writer::from_writer(vec![]);
            club_data.iter().try_for_each(|(_, data)| {
                writer.serialize(data)?;

                Ok::<(), Box<dyn std::error::Error>>(())
            })?;

            let data = String::from_utf8(writer.into_inner()?)?;
            let mut file = File::create("./data/youth_contribution.csv")?;
            file.write_all(data.as_bytes())?;
        }

        {
            let mut writer = csv::Writer::from_writer(vec![]);
            nine_hundred_players.iter().try_for_each(|player| {
                writer.serialize(player)?;
                Ok::<(), Box<dyn std::error::Error>>(())
            })?;

            let data = String::from_utf8(writer.into_inner()?)?;
            let mut file = File::create("./data/nine_hundred_players.csv")?;
            file.write_all(data.as_bytes())?;
        }

        {
            let mut writer = csv::Writer::from_writer(vec![]);
            all_youth_minutes.iter().try_for_each(|data| {
                writer.serialize(data)?;
                Ok::<(), Box<dyn std::error::Error>>(())
            })?;

            let data = String::from_utf8(writer.into_inner()?)?;
            let mut file = File::create("./data/all_youth_players_minutes.csv")?;
            file.write_all(data.as_bytes())?;
        }
    }
    Ok(())
}

#[allow(unused)]
pub struct Query<const N: usize> {
    tier: CompetitionTier,
    season: &'static str,
    clubs: [ClubName; N],
}

#[allow(unused)]
const S2425: Query<18> = Query {
    tier: CompetitionTier::BRILiga1,
    season: "2024/25",
    clubs: [
        ClubName::PersibBandung,
        ClubName::PersijaJakarta,
        ClubName::DewaUnited,
        ClubName::PersebayaSurabaya,
        ClubName::PSMMakassar,
        ClubName::PersikKediri,
        ClubName::Arema,
        ClubName::BaliUnited,
        ClubName::PersitaTangerang,
        ClubName::BorneoFC,
        ClubName::SemenPadang,
        ClubName::MaduraUnited,
        ClubName::PSBSBiak,
        ClubName::PersisSolo,
        ClubName::MalutUnited,
        ClubName::PSISSemarang,
        ClubName::PSSSleman,
        ClubName::BaritoPutera,
    ],
};

const S2526: Query<18> = Query {
    tier: CompetitionTier::BRILiga1,
    season: "2025/26",
    clubs: [
        ClubName::PersibBandung,
        ClubName::PersijaJakarta,
        ClubName::DewaUnited,
        ClubName::PersebayaSurabaya,
        ClubName::PSMMakassar,
        ClubName::PersikKediri,
        ClubName::Arema,
        ClubName::BaliUnited,
        ClubName::PersitaTangerang,
        ClubName::BorneoFC,
        ClubName::MaduraUnited,
        ClubName::MalutUnited,
        ClubName::Persijap,
        ClubName::PSIM,
        ClubName::Bhayangkara,
        ClubName::PSBSBiak,
        ClubName::PersisSolo,
        ClubName::SemenPadang,
    ],
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = std::env::args();

    match args.nth(1) {
        Some(arg) => match arg.as_str() {
            "ap" => academy_product(&S2526)?,
            "yc" => youth_contribution()?,
            _ => return Err("Unknown command! use ap for academy product, or yc for youth contribution".into())
        }
        _ => return Err("Specify the command! use ap for academy product, or yc for youth contribution".into())
    }

    Ok(())
}
