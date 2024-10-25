package lib

import (
	"context"
	"fmt"
	"io"
	"os"
	"time"

	"cloud.google.com/go/storage"
)

// downloadFile downloads an object to a file.
// bucket := "bucket-name"
// object := "object-name"
// destFileName := "file.txt"
func DownloadFile(bucket, object string, destFileName string) error {
	ctx := context.Background()
	client, err := storage.NewClient(ctx)
	if err != nil {
		return fmt.Errorf("storage.NewClient: %w", err)
	}
	defer client.Close()

	ctx, cancel := context.WithTimeout(ctx, time.Second*50)
	defer cancel()

	destFile, err := os.Create(destFileName)
	if err != nil {
		return fmt.Errorf("os.Create: %w", err)
	}

	objectReader, err := client.Bucket(bucket).Object(object).NewReader(ctx)
	if err != nil {
		return fmt.Errorf("Object(%q).NewReader: %w", object, err)
	}
	defer objectReader.Close()

	if _, err := io.Copy(destFile, objectReader); err != nil {
		return fmt.Errorf("io.Copy: %w", err)
	}

	if err = destFile.Close(); err != nil {
		return fmt.Errorf("f.Close: %w", err)
	}

	// fmt.Fprintln("Blob %v downloaded to local file %v\n", object, destFileName)

	return nil

}
