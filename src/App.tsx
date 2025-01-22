import React from 'react';
import { Play, DollarSign, Heart, Cast, Film } from 'lucide-react';

function App() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Hero Section with Video */}
      <div className="relative h-[70vh]">
      <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent z-10"></div>
        <iframe 
          className="w-full h-full object-cover"
          src="https://www.youtube.com/embed/coKW0ake9SM?autoplay=1&mute=0&loop=1&playlist=coKW0ake9SM&controls=0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-12 -mt-20 relative z-20">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Movie Info */}
          <div className="md:w-2/3">
            <h1 className="text-5xl font-bold mb-4 text-red-600">O Sequestro</h1>
            <div className="flex items-center gap-4 mb-6 text-gray-400">
              <span className="flex items-center gap-2">
                <Film size={20} />
                Diretor: FAYSERVICES
              </span>
              <span className="flex items-center gap-2">
                <Cast size={20} />
                Protagonista: ONDTWE
              </span>
            </div>

            <div className="bg-gray-900 p-6 rounded-lg mb-8">
              <h2 className="text-2xl font-semibold mb-4">Sinopse</h2>
              <p className="text-gray-300 leading-relaxed">
                Uma história emocionante de vingança e amor familiar. ONDTWE, nascido em uma família humilde, 
                vê sua vida transformada quando seu irmão mais novo é sequestrado. Após bandidos descobrirem 
                a riqueza de seu pai na produção de gado, exigem um resgate de 50.000,00MT. O que começa como 
                uma simples negociação se transforma em uma busca implacável por justiça quando os sequestradores 
                alegam ter matado seu irmão.
              </p>
            </div>

            {/* Donation Section */}
            <div className="bg-red-900/30 p-6 rounded-lg">
              <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <Heart className="text-red-500" />
                Apoie este Projeto
              </h2>
              <p className="text-gray-300 mb-6">
                Ajude-nos a continuar produzindo cinema de qualidade em Moçambique. 
                Sua contribuição faz a diferença!
              </p> 
              <div className="flex flex-col sm:flex-row gap-4">
                <button className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg flex items-center justify-center gap-2">
                  <DollarSign size={20} />
                  Doar via M-Pesa
                </button>
                <button className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg flex items-center justify-center gap-2">
                  <DollarSign size={20} />
                  Doar via E-mola
                </button>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="md:w-1/3">
            <div className="bg-gray-900 p-6 rounded-lg sticky top-4">
              <h2 className="text-2xl font-semibold mb-4">Equipe Criativa</h2>
              <ul className="space-y-4 text-gray-300">
                <li>
                  <strong className="text-red-500">Direção:</strong> FAYSERVICES
                </li>
                <li>
                  <strong className="text-red-500">Edição:</strong> FAYSERVICES
                </li>
                <li>
                  <strong className="text-red-500">Protagonista:</strong> ONDTWE
                </li>
                <li>
                  <strong className="text-red-500">Site criado por:</strong> Ghost04
                </li>
              </ul>

              <div className="mt-8">
                <button className="w-full bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg flex items-center justify-center gap-2">
                  <Play size={20} />
                  Assistir Trailer
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
