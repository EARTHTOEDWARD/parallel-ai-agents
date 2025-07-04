import * as path from 'path';
import * as os from 'os';

import * as fs from 'fs-extra';

import { PaperIngestor } from '../../backend/src/ingestor';

// Mock the llmGuard module
jest.mock('../../backend/src/lib/llmGuard', () => ({
  summariseLLM: jest.fn().mockImplementation(async (text: string, meta: unknown) => {
    return {
      meta,
      insights: [
        'Mocked insight 1: Complex systems exhibit emergent behavior',
        'Mocked insight 2: Feedback loops are crucial in system dynamics',
        'Mocked insight 3: Non-linear interactions lead to unpredictability',
        'Mocked insight 4: System boundaries are often arbitrary',
        'Mocked insight 5: Scale matters in complex systems',
      ],
    };
  }),
}));

describe('PaperIngestor', () => {
  let tempDir: string;
  let outputFile: string;
  let ingestor: PaperIngestor;

  beforeEach(async () => {
    // Create temp directories
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'test-ingestor-'));
    outputFile = path.join(tempDir, 'test-insights.md');
    ingestor = new PaperIngestor(tempDir, outputFile);
  });

  afterEach(async () => {
    // Clean up
    await fs.remove(tempDir);
  });

  describe('processOnce', () => {
    it('should process PDF files and append to markdown', async () => {
      // Copy sample file to temp directory
      const sampleFile = path.join(__dirname, '../fixtures/sample.txt');
      const targetFile = path.join(tempDir, 'test-paper.txt');
      await fs.copy(sampleFile, targetFile);

      // Process papers
      await ingestor.processOnce();

      // Check output file exists
      const exists = await fs.pathExists(outputFile);
      expect(exists).toBe(true);

      // Read and verify content
      const content = await fs.readFile(outputFile, 'utf-8');
      expect(content).toContain('## Understanding Complex Systems');
      expect(content).toContain('Jane Smith');
      expect(content).toContain('**Source:** test-paper.txt');
      expect(content).toContain('Complex systems exhibit emergent behavior');
    });

    it('should process TXT files', async () => {
      // Create a text file
      const txtFile = path.join(tempDir, 'research.txt');
      await fs.writeFile(
        txtFile,
        `
        Quantum Computing Research
        by Alice Johnson
        
        This paper discusses quantum computing advances.
      `
      );

      await ingestor.processOnce();

      const content = await fs.readFile(outputFile, 'utf-8');
      expect(content).toContain('Quantum Computing Research');
      expect(content).toContain('Alice Johnson');
    });

    it('should skip non-PDF/TXT files', async () => {
      // Create files with different extensions
      await fs.writeFile(path.join(tempDir, 'image.png'), 'fake image data');
      await fs.writeFile(path.join(tempDir, 'document.docx'), 'fake docx data');

      await ingestor.processOnce();

      // Output file should not exist since no valid files were processed
      const exists = await fs.pathExists(outputFile);
      expect(exists).toBe(false);
    });

    it('should handle empty directory', async () => {
      await expect(ingestor.processOnce()).resolves.not.toThrow();
    });
  });

  describe('processPaper', () => {
    it('should extract metadata correctly', async () => {
      const txtFile = path.join(tempDir, 'paper.txt');
      await fs.writeFile(
        txtFile,
        `
        Machine Learning in Healthcare
        Authors: Dr. Sarah Lee, Prof. Michael Chen
        
        Abstract: This study explores ML applications in medical diagnosis.
      `
      );

      await ingestor.processPaper(txtFile);

      const content = await fs.readFile(outputFile, 'utf-8');
      expect(content).toContain('Machine Learning in Healthcare');
      expect(content).toContain('Dr. Sarah Lee');
      expect(content).toContain('Prof. Michael Chen');
    });

    it('should handle files without clear metadata', async () => {
      const txtFile = path.join(tempDir, 'unnamed.txt');
      await fs.writeFile(txtFile, 'Some research content without clear structure.');

      await ingestor.processPaper(txtFile);

      const content = await fs.readFile(outputFile, 'utf-8');
      expect(content).toContain('unnamed'); // Should use filename as title
      expect(content).toContain('**Authors:** Unknown');
    });
  });

  describe('error handling', () => {
    it('should emit COMPACT_ERROR on processing failure', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

      // Try to process non-existent file
      await expect(ingestor.processPaper('/non/existent/file.pdf')).rejects.toThrow();

      expect(consoleSpy).toHaveBeenCalledWith(
        'COMPACT_ERROR:',
        expect.stringContaining('PROCESSING_FAILED')
      );

      consoleSpy.mockRestore();
    });
  });
});
