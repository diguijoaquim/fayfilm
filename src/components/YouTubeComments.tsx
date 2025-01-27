import React, { useEffect, useState } from 'react';

interface Comment {
  id: string;
  authorDisplayName: string;
  authorProfileImageUrl: string;
  textDisplay: string;
  publishedAt: string;
  likeCount: number;
}

function YouTubeComments() {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(
          `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=coKW0ake9SM&key=AIzaSyAMfJhtPHj7I32jZllDdvIj0RhQnwSdfls&maxResults=100`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch comments');
        }

        const data = await response.json();
        const formattedComments = data.items.map((item: any) => ({
          id: item.id,
          authorDisplayName: item.snippet.topLevelComment.snippet.authorDisplayName,
          authorProfileImageUrl: item.snippet.topLevelComment.snippet.authorProfileImageUrl,
          textDisplay: item.snippet.topLevelComment.snippet.textDisplay,
          publishedAt: item.snippet.topLevelComment.snippet.publishedAt,
          likeCount: item.snippet.topLevelComment.snippet.likeCount
        }));

        setComments(formattedComments);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load comments');
      } finally {
        setLoading(false);
      }
    };

    fetchComments();
  }, []);

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto"></div>
        <p className="mt-4 text-gray-400">Carregando comentários...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8 text-red-500">
        <p>Erro ao carregar comentários: {error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold mb-6">Comentários do YouTube</h2>
      {comments.length === 0 ? (
        <p className="text-gray-400">Nenhum comentário encontrado.</p>
      ) : (
        <div className="space-y-6">
          {comments.map((comment) => (
            <div key={comment.id} className="bg-gray-900/50 p-4 rounded-lg">
              <div className="flex items-start gap-4">
                <img
                  src={comment.authorProfileImageUrl}
                  alt={comment.authorDisplayName}
                  className="w-10 h-10 rounded-full"
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold">{comment.authorDisplayName}</h3>
                    <span className="text-sm text-gray-400">
                      {new Date(comment.publishedAt).toLocaleDateString('pt-BR')}
                    </span>
                  </div>
                  <p className="text-gray-300">{comment.textDisplay}</p>
                  {comment.likeCount > 0 && (
                    <div className="mt-2 text-sm text-gray-400">
                      {comment.likeCount} {comment.likeCount === 1 ? 'curtida' : 'curtidas'}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default YouTubeComments;