use std::{collections::{HashMap, HashSet}, fs::File, io::Write};
use serde::{Serialize, Deserialize};

const DATA: &str = include_str!("../../data/youth_liga1.csv");
const YOUTH_DATA: &str = include_str!("../../data/mop.csv");

#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Eq, Hash)]
enum ClubName {
    #[serde(rename(deserialize = "PSIS Semarang", serialize = "PSIS Semarang"))]
    PSISSemarang,
    #[serde(rename(deserialize = "PSS Sleman", serialize = "PSS Sleman"))]
    PSSSleman,
    #[serde(rename(deserialize = "Persib Bandung", serialize = "Persib Bandung"))]
    PersibBandung,
    #[serde(rename(deserialize = "Barito Putera", serialize = "Barito Putera"))]
    BaritoPutera,
    #[serde(rename(deserialize = "Persik Kediri", serialize = "Persik Kediri"))]
    PersikKediri,
    #[serde(rename(deserialize = "Dewa United", serialize = "Dewa United"))]
    DewaUnited,
    #[serde(rename(deserialize = "Persebaya Surabaya", serialize = "Persebaya Surabaya"))]
    PersebayaSurabaya,
    #[serde(rename(deserialize = "Persija Jakarta", serialize = "Persija Jakarta"))]
    PersijaJakarta,
    #[serde(rename(deserialize = "Arema", serialize = "Arema"))]
    Arema,
    #[serde(rename(deserialize = "PSM Makassar", serialize = "PSM Makassar"))]
    PSMMakassar,
    #[serde(rename(deserialize = "Bali United", serialize = "Bali United"))]
    BaliUnited,
    #[serde(rename(deserialize = "Persita Tangerang", serialize = "Persita Tangerang"))]
    PersitaTangerang,
    #[serde(rename(deserialize = "Borneo FC", serialize = "Borneo FC"))]
    BorneoFC,
    #[serde(rename(deserialize = "Semen Padang", serialize = "Semen Padang"))]
    SemenPadang,
    #[serde(rename(deserialize = "Madura United", serialize = "Madura United"))]
    MaduraUnited,
    #[serde(rename(deserialize = "PSBS Biak", serialize = "PSBS Biak"))]
    PSBSBiak,
    #[serde(rename(deserialize = "Persis Solo", serialize = "Persis Solo"))]
    PersisSolo,
    #[serde(rename(deserialize = "Malut United", serialize = "Malut United"))]
    MalutUnited,
}

impl From<String> for ClubName {
    fn from(value: String) -> Self {
        match value.as_str() {
            "PSIS Semarang" => Self::PSISSemarang,
            "PSS Sleman" => Self::PSSSleman,
            "PERSIB Bandung" => Self::PersibBandung,
            "PS Barito Putera" => Self::BaritoPutera,
            "PERSIK Kediri" => Self::PersikKediri,
            "Dewa United FC" => Self::DewaUnited,
            "PERSEBAYA Surabaya" => Self::PersebayaSurabaya,
            "PERSIJA Jakarta" => Self::PersijaJakarta,
            "AREMA FC" => Self::Arema,
            "PSM Makassar" => Self::PSMMakassar,
            "Bali United FC" => Self::BaliUnited,
            "PERSITA Tangerang" => Self::PersitaTangerang,
            "Borneo FC Samarinda" => Self::BorneoFC,
            "Semen Padang FC" => Self::SemenPadang,
            "Madura United FC" => Self::MaduraUnited,
            "PSBS Biak" => Self::PSBSBiak,
            "PERSIS Solo" => Self::PersisSolo,
            "Malut United FC" => Self::MalutUnited,
            n => {
                eprintln!("unrecognized club: {n}");
                unreachable!()
            }
        }
    }
}

impl std::fmt::Display for ClubName {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let s = match self {
            ClubName::PSISSemarang => "PSIS Semarang",
            ClubName::PSSSleman => "PSS Sleman",
            ClubName::PersibBandung => "Persib Bandung",
            ClubName::BaritoPutera => "Barito Putera",
            ClubName::PersikKediri => "Persik Kediri",
            ClubName::DewaUnited => "Dewa United",
            ClubName::PersebayaSurabaya => "Persebaya Surabaya",
            ClubName::PersijaJakarta => "Persija Jakarta",
            ClubName::Arema => "Arema",
            ClubName::PSMMakassar => "PSM Makassar",
            ClubName::BaliUnited => "Bali United",
            ClubName::PersitaTangerang => "Persita Tangerang",
            ClubName::BorneoFC => "Borneo FC",
            ClubName::SemenPadang => "Semen Padang",
            ClubName::MaduraUnited => "Madura United",
            ClubName::PSBSBiak => "PSBS Biak",
            ClubName::PersisSolo => "Persis Solo",
            ClubName::MalutUnited => "Malut United",
        };
        write!(f, "{s}")
    }
}

impl std::fmt::Debug for ClubName {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

#[derive(Debug, Serialize, Deserialize, Clone, Copy)]
enum Position {
    GK,
    DF,
    MF,
    WG,
    FW,
    NP,
}

#[derive(Debug, Serialize, Deserialize, PartialEq, Eq, Clone, Copy)]
enum Competition {
    #[serde(rename(deserialize = "BRI Liga 1"))]
    BRILiga1,
    #[serde(rename(deserialize = "Pegadaian Liga 2"))]
    PegadaianLiga2
}

#[derive(Debug, Serialize, Deserialize)]
struct Row {
    #[serde(rename(deserialize = "Club now"))]
    club_now: String,
    #[serde(rename(deserialize = "Name"))]
    name: String,
    #[serde(rename(deserialize = "DOB"))]
    dob: String,
    #[serde(rename(deserialize = "Pos"))]
    pos: Position,
    #[serde(rename(deserialize = "Minutes"))]
    minutes: f32,
    #[serde(rename(deserialize = "Games"))]
    games: f32,
    #[serde(rename(deserialize = "Youth Club"))]
    youth_club: ClubName,
    #[serde(rename(deserialize = "Competition"))]
    competition: Competition,
}

#[derive(Debug)]
struct ApData {
    club_now: String,
    dob: String,
    pos: Position,
    minutes: f32,
    games: f32,
    youth_club: HashSet<ClubName>,
    competition: Competition,
}

#[derive(Debug, Serialize)]
struct Player {
    #[serde(rename(serialize = "Player Name"))]
    name: String,
    #[serde(rename(serialize = "DOB"))]
    dob: String,
    #[serde(rename(serialize = "Pos"))]
    pos: Position,
    #[serde(rename(serialize = "Minutes"))]
    minutes: f32,
    #[serde(rename(serialize = "Games"))]
    games: f32,
    #[serde(rename(serialize = "Club Now"))]
    club_now: String,
    #[serde(rename(serialize = "Competition"))]
    competition: Competition,
    #[serde(rename(serialize = "Youth Clubs"))]
    youth_clubs: u8,
}

#[derive(Debug, Serialize)]
struct YouthClub {
    #[serde(rename(serialize = "Club Name"))]
    club_name: ClubName,
    #[serde(rename(serialize = "Players Registered"))]
    players_count: usize,
    #[serde(rename(serialize = "Players with Minutes"))]
    players_with_minutes: usize,
    #[serde(rename(serialize = "Adjusted Total Games"))]
    games: u32,
    #[serde(rename(serialize = "Adjusted Total Minutes"))]
    minutes: u32,
    #[serde(skip)]
    players: Vec<Player>,
}

fn get_ap_data<F>(player_data: HashMap<String, ApData>, f: F) -> HashMap<ClubName, YouthClub>
where
    F: FnMut(&(&String, &ApData)) -> bool,
{
    let mut youth_clubs: HashMap<ClubName, YouthClub> = HashMap::new();
    youth_clubs.insert(ClubName::MalutUnited, YouthClub {
        club_name: ClubName::MalutUnited,
        players_count: 0,
        players_with_minutes: 0,
        games: 0,
        minutes: 0,
        players: Vec::new(),
    });

    player_data
        .iter()
        .filter(f)
        .for_each(|(name, data)| {
            let len = data.youth_club.len() as f32;
            let minutes = data.minutes / len;
            let games = data.games / len;

            for club in &data.youth_club {
                youth_clubs
                    .entry(*club)
                    .and_modify(|yc| {
                        yc.minutes += minutes.round() as u32;
                        yc.games += games.round() as u32;
                        yc.players_count += 1;
                        if data.minutes > 0. {
                            yc.players_with_minutes += 1;
                        }
                        yc.players.push(Player {
                            name: name.clone(),
                            dob: data.dob.clone(),
                            minutes: data.minutes,
                            games: data.games,
                            pos: data.pos,
                            club_now: data.club_now.clone(),
                            competition: data.competition,
                            youth_clubs: len as u8,
                        });
                    })
                    .or_insert(YouthClub {
                        club_name: *club,
                        players_count: 1,
                        players_with_minutes: {
                            if data.minutes > 0. { 1 } else { 0 }
                        },
                        games: games.round() as u32,
                        minutes: minutes.round() as u32,
                        players: {
                            let mut vec = vec![];
                            vec.push(Player {
                                name: name.clone(),
                                dob: data.dob.clone(),
                                minutes: data.minutes,
                                games: data.games,
                                pos: data.pos,
                                club_now: data.club_now.clone(),
                                competition: data.competition,
                                youth_clubs: len as u8,
                            });
                            vec
                        },
                    });
            }
        });

    youth_clubs
}

fn academy_product() -> Result<(), Box<dyn std::error::Error>> {
    let mut df = csv::Reader::from_reader(DATA.as_bytes());
    let mut iter = df.deserialize();
    let mut player_data: HashMap<String, ApData> = HashMap::new();

    while let Some(record) = iter.next() {
        let row: Row = record?;
        player_data.entry(row.name)
            .and_modify(|data| {
                data.youth_club.insert(row.youth_club);
            })
            .or_insert(ApData {
                club_now: row.club_now,
                dob: row.dob,
                pos: row.pos,
                minutes: row.minutes,
                games: row.games,
                youth_club: {
                    let mut h = HashSet::new();
                    h.insert(row.youth_club);
                    h
                },
                competition: row.competition,
            });
    }

    let youth_clubs = get_ap_data(player_data, |(_, data)| {
        data.competition == Competition::BRILiga1 || data.competition == Competition::PegadaianLiga2
    });

    let mut writer = csv::Writer::from_writer(vec![]);
    youth_clubs.iter().try_for_each(|(_, data)| {
        writer.serialize(data)?;

        Ok::<(), Box<dyn std::error::Error>>(())
    })?;
    let data = String::from_utf8(writer.into_inner()?)?;
    // eprintln!("{data}");

    let mut file = File::create("../data/data.csv")?;
    file.write_all(data.as_bytes())?;

    Ok(())
}

#[derive(Debug, Serialize)]
struct YouthMinutes {
    #[serde(rename(serialize = "Team"))]
    club_name: ClubName,
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
    #[serde(rename(deserialize = "Team"))]
    team: String,
    #[serde(rename(deserialize = "MoP"))]
    minutes: u32,
    #[serde(rename(deserialize = "Age"))]
    age: u8,
    #[serde(rename(deserialize = "Nationality"))]
    nationality: String,
}

#[derive(Debug, Serialize)]
struct AllYouthMinutes {
    #[serde(rename(serialize = "Name"))]
    name: String,
    #[serde(rename(serialize = "Team"))]
    team: ClubName,
    #[serde(rename(serialize = "MoP"))]
    minutes: u32,
}

#[derive(Debug, Serialize)]
struct NineHundred {
    #[serde(rename(serialize = "Name"))]
    name: String,
    #[serde(rename(serialize = "Team"))]
    club_name: ClubName,
    #[serde(rename(serialize = "Minutes"))]
    minutes: u32,
}

fn youth_contribution() -> Result<(), Box<dyn std::error::Error>> {
    let mut df = csv::Reader::from_reader(YOUTH_DATA.as_bytes());
    let mut iter = df.deserialize();
    let mut club_data: HashMap<ClubName, YouthMinutes> = HashMap::new();
    let mut nine_hundred_players = vec![];
    let mut all_youth_minutes = vec![];

    while let Some(record) = iter.next() {
        let row: MoP = record?;
        let club_name: ClubName = row.team.into();
        if row.nationality == "Indonesia" && row.age <= 22 {
            all_youth_minutes.push(AllYouthMinutes {
                name: row.name.clone(),
                team: club_name,
                minutes: row.minutes,
            });
            if row.minutes >= 900 {
                nine_hundred_players.push(NineHundred {
                    name: row.name.clone(),
                    club_name,
                    minutes: row.minutes,
                });
            }
            club_data.entry(club_name)
                .and_modify(|youth| {
                    if row.minutes > 0 {
                        youth.players_with_minutes += 1
                    }
                    if row.minutes >= 900 {
                        youth.nine_hundred += 1;
                    }
                    youth.total_minutes += row.minutes;
                })
                .or_insert(YouthMinutes {
                    club_name,
                    players_with_minutes: {
                        if row.minutes > 0 { 1 } else { 0 }
                    },
                    total_minutes: row.minutes,
                    nine_hundred: {
                        if row.minutes >= 900 { 1 } else { 0 }
                    },
                });
        }
        {
            let mut writer = csv::Writer::from_writer(vec![]);
            club_data.iter().try_for_each(|(_, data)| {
                writer.serialize(data)?;

                Ok::<(), Box<dyn std::error::Error>>(())
            })?;

            let data = String::from_utf8(writer.into_inner()?)?;
            let mut file = File::create("../data/youth.csv")?;
            file.write_all(data.as_bytes())?;
        }

        {
            let mut writer = csv::Writer::from_writer(vec![]);
            nine_hundred_players.iter().try_for_each(|player| {
                writer.serialize(player)?;
                Ok::<(), Box<dyn std::error::Error>>(())
            })?;

            let data = String::from_utf8(writer.into_inner()?)?;
            let mut file = File::create("../data/nine_hundred_players.csv")?;
            file.write_all(data.as_bytes())?;
        }

        {
            let mut writer = csv::Writer::from_writer(vec![]);
            all_youth_minutes.iter().try_for_each(|data| {
                writer.serialize(data)?;
                Ok::<(), Box<dyn std::error::Error>>(())
            })?;

            let data = String::from_utf8(writer.into_inner()?)?;
            let mut file = File::create("../data/all_youth_minutes.csv")?;
            file.write_all(data.as_bytes())?;
        }
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = std::env::args();

    match args.nth(1) {
        Some(arg) if arg == "ap" => academy_product()?,
        _ => youth_contribution()?,
    }

    Ok(())
}
