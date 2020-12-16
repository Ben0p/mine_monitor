import psycopg2


conn = psycopg2.connect(dbname='mmodel_sol', port=5432, user='postgres',
                            password='*8Bv[a#Y%_', host='pthgeorep01.fmg.local')

cur = conn.cursor()

points = cur.execute("SELECT * FROM public.ms_nams ORDER BY gid ASC LIMIT 100")

print(len(points))