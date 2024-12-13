import os
import re
from multiprocessing import Pool, cpu_count


def replace_in_file(file_path, old_url, new_url):
    """Replace old_url with new_url in a single file."""
    try:
        # Read the file's content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace the old URL with the new URL
        updated_content = re.sub(re.escape(old_url), new_url, content)

        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def process_files(file_paths, old_url, new_url):
    """Process a batch of files."""
    for file_path in file_paths:
        replace_in_file(file_path, old_url, new_url)


def main(directory, old_url, new_url):
    """Main function to parallelize file processing."""
    # Collect all files in the directory
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            # Skip non-text files
            if not file.endswith(('.html', '.htm', '.css', '.js', '.txt')):
                continue
            all_files.append(os.path.join(root, file))

    # Split files into chunks for multiprocessing
    num_cpus = cpu_count()
    chunk_size = len(all_files) // num_cpus + 1
    file_chunks = [all_files[i:i + chunk_size] for i in range(0, len(all_files), chunk_size)]

    # Create a pool of workers
    with Pool(num_cpus) as pool:
        pool.starmap(process_files, [(chunk, old_url, new_url) for chunk in file_chunks])


# Parameters
if __name__ == "__main__":
    downloaded_directory = "/Users/natko.gluscevic/www.d20pfsrd.com"
    old_base_url = "www.d20pfsrd.com"
    new_base_url = "www.google.com"

    main(downloaded_directory, old_base_url, new_base_url)