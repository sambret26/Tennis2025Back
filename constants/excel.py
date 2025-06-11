# [FILE SETTINGS]
EXCEL_FILENAME = "Tournoi_Royans_Vercors_2025.xlsx"
MATCHES_SHEET_NAME = "Matchs"
SCHEDULE_SHEET_NAME = "Programmation"
PLAYERS_SHEET_NAME = "Joueurs"
PLAYERS_HEADERS = ["Joueur", "Classement", None, "Equipe", "Classement"]
PLAYERS_COLUMN_WIDTHS = [30, 12, 5, 30, 12]
MATCHES_HEADERS = ["Num", "Joueur1", "Cl", "Joueur2", "Cl", "Tableau", "Vainqueur", "Score", "Suivant"]
MATCHES_COLUMN_WIDTHS = [7, 27, 5, 27, 5, 8, 27, 18, 10]
SCHEDULE_HEADERS = ["Jour", "Heure", "Terrain", "Numéro", "Joueur/Equipe", "Classement", "Joueur/Equipe", "Classement", "Tableau", "Vainqueur", "Score", "Suivant"]
SCHEDULE_COLUMN_WIDTHS = [15, 12, 12, 8, 27, 10, 27, 10, 9, 27, 12, 10]

# [FORMULAS]
MATCHS_FORMULA_COLUMN_C = "=IFERROR(VLOOKUP(BROWNUM,Joueurs!$A$2:$B$200,2,0), IFERROR(VLOOKUP(BROWNUM,Joueurs!$D$2:$E$200,2,0),0))"
MATCHS_FORMULA_COLUMN_E = "=IFERROR(VLOOKUP(DROWNUM,Joueurs!$A$2:$B$200,2,0), IFERROR(VLOOKUP(DROWNUM,Joueurs!$D$2:$E$200,2,0),0))"
SCHEDULE_FORMULA = "=IF(DROWNUM<>0, VLOOKUP(DROWNUM, Matchs!$A$1:$M$199, COLUMN, 0), 0)"

# [HOURS]
WEEK_START_HOUR = "16H30"
WEEKEND_START_HOUR = "7H30"
MAX_HOUR = "22H30"

# [ERRORS]
SHEET_NOT_FOUND = "La page SHEET_NAME n'est pas présente, le fichier est refusé"
