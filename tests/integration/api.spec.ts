import request from 'supertest';
import { createServer } from 'http';
import { parse } from 'url';
import next from 'next';
import * as fs from 'fs-extra';
import * as path from 'path';

describe('API Integration Tests', () => {
  let server: any;
  let app: any;

  beforeAll(async () => {
    // Setup Next.js in test mode
    app = next({ dev: false, dir: path.join(__dirname, '../../frontend') });
    const handle = app.getRequestHandler();
    await app.prepare();

    server = createServer((req, res) => {
      const parsedUrl = parse(req.url!, true);
      handle(req, res, parsedUrl);
    });
  });

  afterAll(async () => {
    await app.close();
  });

  describe('GET /api/insights', () => {
    it('should return insights when markdown file exists', async () => {
      // Create test markdown file
      const insightsPath = path.join(__dirname, '../../docs/research-insights.md');
      await fs.ensureDir(path.dirname(insightsPath));
      await fs.writeFile(insightsPath, `
## Test Paper 1
- **Authors:** Test Author
- **Source:** test.pdf
- **Key insights:**
  - Test insight 1
  - Test insight 2

## Test Paper 2
- **Authors:** Another Author, Co-Author
- **Source:** research.pdf
- **Key insights:**
  - Research finding 1
  - Research finding 2
  - Research finding 3
      `);

      const response = await request(server)
        .get('/api/insights')
        .expect(200);

      expect(response.body).toHaveLength(2);
      expect(response.body[0].meta.title).toBe('Test Paper 1');
      expect(response.body[0].meta.authors).toEqual(['Test Author']);
      expect(response.body[0].insights).toHaveLength(2);
      
      expect(response.body[1].meta.title).toBe('Test Paper 2');
      expect(response.body[1].meta.authors).toEqual(['Another Author', 'Co-Author']);
      expect(response.body[1].insights).toHaveLength(3);

      // Clean up
      await fs.remove(insightsPath);
    });

    it('should return 404 when insights file does not exist', async () => {
      // Ensure file doesn't exist
      const insightsPath = path.join(__dirname, '../../docs/research-insights.md');
      await fs.remove(insightsPath).catch(() => {});

      const response = await request(server)
        .get('/api/insights')
        .expect(404);

      expect(response.body).toEqual({ error: 'Insights file not found' });
    });

    it('should handle empty markdown file', async () => {
      const insightsPath = path.join(__dirname, '../../docs/research-insights.md');
      await fs.ensureDir(path.dirname(insightsPath));
      await fs.writeFile(insightsPath, '');

      const response = await request(server)
        .get('/api/insights')
        .expect(200);

      expect(response.body).toEqual([]);

      await fs.remove(insightsPath);
    });

    it('should only accept GET requests', async () => {
      await request(server)
        .post('/api/insights')
        .expect(405);

      await request(server)
        .put('/api/insights')
        .expect(405);

      await request(server)
        .delete('/api/insights')
        .expect(405);
    });
  });
});