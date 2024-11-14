import os, sys



dataset = DataLoadFactory().get_dataset(
    load_type=LoadType.LOCAL,
    path=os.path.join(BASE_DIR, 'crawler', 'output', 'GIAS_Portuguese_IIA.csv')
)