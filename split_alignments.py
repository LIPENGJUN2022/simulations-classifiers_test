import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def split_alignment(input_file, output_dir):
    """
    将FASTA对齐文件分割成单独的序列文件
    
    Args:
        input_file (str): 输入FASTA文件的路径
        output_dir (str): 输出目录的路径
    """
    # 获取输入文件的文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # 读取FASTA文件
    for record in SeqIO.parse(input_file, "fasta"):
        # 创建新的序列记录
        new_record = SeqRecord(
            seq=record.seq,
            id=record.id,
            description=record.description
        )
        
        # 创建输出文件名
        output_file = os.path.join(output_dir, f"{base_name}_{record.id}.fasta")
        
        # 写入单个序列文件
        SeqIO.write(new_record, output_file, "fasta")
        print(f"已创建文件: {output_file}")

def process_fasta_dir(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith('.fasta'):
            input_file = os.path.join(input_dir, filename)
            print(f"\n处理文件: {input_file}")
            split_alignment(input_file, output_dir)
    print(f"\n所有序列文件已保存到: {output_dir}")

def process_main_folder(main_folder):
    # 处理 real/gap_and_ambigless
    real_gap = os.path.join(main_folder, 'real', 'gap_and_ambigless')
    if os.path.exists(real_gap):
        outdir = os.path.join(main_folder, 'real', 'gap_and_ambigless_split_seq')
        print(f"\n处理: {real_gap} -> {outdir}")
        process_fasta_dir(real_gap, outdir)
    # 处理 simulation 下的所有子文件夹
    sim_dir = os.path.join(main_folder, 'simulation')
    if os.path.exists(sim_dir):
        sim_outdir = os.path.join(main_folder, 'simulation_split_seq')
        for sub in os.listdir(sim_dir):
            sub_path = os.path.join(sim_dir, sub)
            if os.path.isdir(sub_path):
                outdir = os.path.join(sim_outdir, sub)
                print(f"\n处理: {sub_path} -> {outdir}")
                process_fasta_dir(sub_path, outdir)

def main():
    if len(sys.argv) < 2:
        print("用法: python split_alignments.py data_mammals [data_viridiplantae ...]")
        sys.exit(1)
    for folder in sys.argv[1:]:
        if not os.path.exists(folder):
            print(f"错误: 目录 {folder} 不存在")
            continue
        print(f"\n==== 处理主目录: {folder} ====")
        process_main_folder(folder)
    print("\n全部处理完成！")

if __name__ == "__main__":
    main() 