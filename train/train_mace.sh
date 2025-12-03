# Training from scratch (TS)
mace_run_train --name="MACE" --r_max=6.0 --MLP_irreps="16x0e" --max_L=0 --energy_key="energy" --forces_key="forces" --train_file=./train.extxyz --valid_fraction=0.2 --test_file=./test.extxyz --forces_weight=10.0 --E0s="average" --lr=0.02 --scaling="rms_forces_scaling" --batch_size=4 --max_num_epochs=200 --ema --eval_interval=1 --seed=0

# Fine-tuning (FT)
mace_run_train --name="MACE" --energy_key="energy" --forces_key="forces" --foundation_model=./2023-12-10-mace-128-L0_energy_epoch-249.model --train_file=./train.extxyz --valid_fraction=0.2 --test_file=./test.extxyz --forces_weight=10.0 --E0s="average" --lr=0.001 --scaling="rms_forces_scaling" --batch_size=4 --max_num_epochs=20 --ema --eval_interval=1 --seed=0

# Multi-head fine-tuning (MHFT)
mace_run_train --multiheads_finetuning="True" --weight_pt=0.1 --name="MACE" --energy_key="energy" --forces_key="forces" --foundation_model=./2023-12-10-mace-128-L0_energy_epoch-249.model --pt_train_file=./pretrain.extxyz --train_file=./train.extxyz --valid_fraction=0.2 --test_file=./test.extxyz --forces_weight=10.0 --E0s="foundation" --lr=0.001 --scaling="rms_forces_scaling" --batch_size=4 --max_num_epochs=20 --ema --eval_interval=1 --seed=0
