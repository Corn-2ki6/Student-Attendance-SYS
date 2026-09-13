# Test database package

## Included test data
- 50 students
- 1 lecturer
- 5 courses / 5 class sections
- 250 enrollments
- weekly schedules
- OPEN / CLOSED / SCHEDULED sessions
- password attendance
- history / percentage / report data

## Accounts
- Student: `student01` / `123456`
- Other students: `student02` ... `student50` / `123456`
- Lecturer: `lecturer01` / `123456`
- `student01` email: `john@gmail.com`
- `student01` student code: `S123`
- Attendance password: `Pass@123`

## Put in the repo
Copy these files into your project:
- `backend/db/init.sql`
- `backend/docker-compose.yml`
- `backend/.env.example`

Create local `backend/.env` from `.env.example`. Do not commit `.env`.

## Run from a fresh database
MySQL only executes `/docker-entrypoint-initdb.d` scripts on a fresh volume.

From `backend/`:
```powershell
docker compose down -v
docker compose up -d
```

Then run backend:
```powershell
$env:DATABASE_URL="mysql+pymysql://attendance_user:attendance_password@127.0.0.1:3307/student_attendance"
$env:JWT_SECRET_KEY="student-attendance-secret-key-2026"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

No manual database creation/import is needed.

## Seeded sessions
- Session 1: OPEN, SELF_SUBMIT, student01 not marked -> TC14
- Session 2: CLOSED -> TC15
- Session 3: OPEN, PASSWORD=`Pass@123` -> TC16/TC17
- Session 4: OPEN, student01 already marked -> TC18
- Session 5: SCHEDULED -> TC23
- Session 6: OPEN with partial attendance -> TC24/TC25/TC26/TC28
- Sessions 7-10: Mathematics 101, Oct 2023 -> TC12/TC27
- Sessions 11-16: CS1 attendance history -> TC12/TC13

## Important conflict in the provided Excel test cases
TC01 requires `student01` to already exist so login can succeed.
TC03 also tries to register `student01` and expects success.
Those two states cannot both be true in the same persistent database.

For TC03 use:
- Name: New Student
- Email: `newstudent@gmail.com`
- Username: `student51`
- Password: `123456`

Then TC04 can repeat the same username/email to verify duplicate rejection.

## Commit these
- `backend/db/init.sql`
- `backend/docker-compose.yml`
- `backend/.env.example`

Do not commit:
- `backend/.env`
- Docker/MySQL data volume
