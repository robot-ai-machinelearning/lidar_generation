import os
import sys
import time

import numpy as np

BASE_DIR = "/mnt/data/lpagec/lidar_baseline"

# choose representation
polar, xyz = 0, 1
rep = "polar" if polar else "xyz"
no_polar = 1 if xyz else 0

runs = 10
run_counter = 0
ran_exps = []
collisions = 0

while run_counter < runs:

    bs = [128, 64, 32]
    p = [0.2, 0.4, 0.4]
    bs = np.random.choice(bs, 1, p=p)[0]

    # glr
    gen_lr = [1e-3, 5e-4]
    p = [0.5, 0.5]
    gen_lr = np.random.choice(gen_lr, 1, p=p)[0]

    # z size
    z_dim = [128, 256, 512]
    p = [1.0 / 3] * 3
    z_dim = np.random.choice(z_dim, 1, p=p)[0]

    base_dir = "%(BASE_DIR)s/%(rep)s_Z%(z_dim)s_BS%(bs)s_GLR%(gen_lr)s" % locals()

    print(base_dir)

    command = (
        "vae_2d.py \
        --base_dir %(base_dir)s \
        --lr %(gen_lr)s \
        --batch_size %(bs)s \
        --z_dim %(z_dim)s \
        --no_polar %(no_polar)s "
        % locals()
    )

    print(command)

    if "mnt" in base_dir:
        command = f" python {command}"
    else:
        command = f"{sys.argv[1]} cc_launch_gan.sh {command}"
    print(command)

    if base_dir not in ran_exps:
        ran_exps += [base_dir]
        os.system(command)
        time.sleep(1)
        run_counter += 1
    else:
        print("run %s has already been launched! %d" % (base_dir, len(ran_exps)))
        collisions += 1

print("%d exps launched and %d collisions" % (runs, collisions))
