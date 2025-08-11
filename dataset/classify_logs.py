import sys
import pandas as pd
import joblib
import time
import os
import numpy as np

def main():
    start_time = time.time()
    
    if len(sys.argv) != 4:
        print("Usage: python classify_logs.py <input_csv> <output_csv> <model_file>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    model_file = sys.argv[3]
    
    # Get file size
    file_size_gb = os.path.getsize(input_csv) / (1024 ** 3)
    print(f"Input file size: {file_size_gb:.2f} GB")
    
    # Determine appropriate chunk size based on file size and available memory
    # This is a rough estimate - adjust based on your system's available memory
    if file_size_gb > 1:  # For files larger than 1GB
        chunksize = 100000  # Process 100,000 rows at a time
        print(f"Large file detected. Processing in chunks of {chunksize} rows")
    else:
        chunksize = None  # Process whole file at once
    
    # Load the trained model
    model_load_start = time.time()
    model = joblib.load(model_file)
    feature_columns = joblib.load("feature_columns.joblib")
    # df = df.reindex(columns=feature_columns, fill_value=0)
    model_load_time = time.time() - model_load_start
    print(f"Model loaded in {model_load_time:.2f} seconds")
    
    if chunksize is None:
        # Process whole file at once (original approach)
        process_whole_file(input_csv, output_csv, model, feature_columns)
    else:
        # Process file in chunks
        process_file_in_chunks(input_csv, output_csv, model, feature_columns, chunksize)
    
    total_time = time.time() - start_time
    print(f"Total processing time: {total_time:.2f} seconds")

def process_whole_file(input_csv, output_csv, model, feature_columns):
    # Load processed data
    data_load_start = time.time()
    df = pd.read_csv(input_csv)
    data_load_time = time.time() - data_load_start
    print(f"Data loaded: {len(df)} rows in {data_load_time:.2f} seconds")
    
    # Data preparation
    prep_start = time.time()
    X = df.drop(columns=['attack_label'], errors='ignore')
    X = X.fillna(0)
    prep_time = time.time() - prep_start
    print(f"Data preparation completed in {prep_time:.2f} seconds")
    
    # Predict
    predict_start = time.time()
    predictions = model.predict(X)
    predict_time = time.time() - predict_start
    print(f"Prediction completed in {predict_time:.2f} seconds for {len(X)} rows")
    print(f"Average prediction time: {predict_time/len(X)*1000:.4f} ms per row")
    
    df['predicted_label'] = predictions
    
    # Save results
    save_start = time.time()
    df.to_csv(output_csv, index=False)
    save_time = time.time() - save_start
    print(f"Results saved to {output_csv} in {save_time:.2f} seconds")

def process_file_in_chunks(input_csv, output_csv, model, feature_columns, chunksize):
    # Create header in output file (first time only)
    header = True
    
    # Stats tracking
    total_rows = 0
    total_predict_time = 0
    
    # Process in chunks
    for chunk_num, chunk in enumerate(pd.read_csv(input_csv, chunksize=chunksize)):
        chunk_start = time.time()
        
        # Data preparation
        X = chunk.drop(columns=['attack_label'], errors='ignore')
        X = X.fillna(0)
        
        # Predict
        predict_start = time.time()
        predictions = model.predict(X)
        chunk_predict_time = time.time() - predict_start
        total_predict_time += chunk_predict_time
        
        chunk['predicted_label'] = predictions
        total_rows += len(chunk)
        
        # Write chunk to output file
        mode = 'w' if header else 'a'
        chunk.to_csv(output_csv, mode=mode, header=header, index=False)
        header = False  # Only write header once
        
        chunk_time = time.time() - chunk_start
        print(f"Chunk {chunk_num+1}: Processed {len(chunk)} rows in {chunk_time:.2f} seconds")
    
    print(f"All chunks processed: {total_rows} total rows")
    print(f"Total prediction time: {total_predict_time:.2f} seconds")
    print(f"Average prediction time: {total_predict_time/total_rows*1000:.4f} ms per row")

if __name__ == "__main__":
    main()