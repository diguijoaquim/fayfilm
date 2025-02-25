import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, DollarSign, ArrowLeft, Copy, Check } from 'lucide-react';

function DonatePage() {
  const navigate = useNavigate();
  const [copiedMpesa, setCopiedMpesa] = useState(false);
  const [copiedEmola, setCopiedEmola] = useState(false);

  const handleCopy = async (text: string, type: 'mpesa' | 'emola') => {
    try {
      await navigator.clipboard.writeText(text);
      if (type === 'mpesa') {
        setCopiedMpesa(true);
        setTimeout(() => setCopiedMpesa(false), 2000);
      } else {
        setCopiedEmola(true);
        setTimeout(() => setCopiedEmola(false), 2000);
      }
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white py-12">
      <div className="max-w-4xl mx-auto px-4">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-gray-400 hover:text-white mb-8"
        >
          <ArrowLeft size={20} />
          Voltar
        </button>

        <div className="bg-gray-900 rounded-lg p-8">
          <div className="flex items-center gap-3 mb-6">
            <Heart className="text-red-500" size={32} />
            <h1 className="text-4xl font-bold">Apoie O Sequestro</h1>
          </div>

          <div className="space-y-8">
            <section>
              <h2 className="text-2xl font-semibold mb-4">Por que doar?</h2>
              <div className="space-y-4 text-gray-300">
                <p>
                  Sua doação é fundamental para o desenvolvimento do cinema moçambicano. 
                  Com o seu apoio, podemos:
                </p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>Continuar produzindo filmes de qualidade</li>
                  <li>Investir em equipamentos e tecnologia</li>
                  <li>Criar oportunidades para novos talentos</li>
                  <li>Contar histórias autênticas de Moçambique</li>
                  <li>Desenvolver a indústria cinematográfica local</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold mb-4">Como doar</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-blue-900/30 p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <DollarSign className="text-blue-400" />
                    M-Pesa
                  </h3>
                  <p className="text-gray-300 mb-4">
                    Para doar via M-Pesa, envie sua contribuição para:
                  </p>
                  <div className="space-y-2">
                    <div className="bg-blue-950/50 p-4 rounded-lg">
                      <p className="text-lg text-gray-300 mb-2">Nome:</p>
                      <p className="text-xl font-semibold">Francisco Agostinho</p>
                    </div>
                    <div className="bg-blue-950/50 p-4 rounded-lg relative group">
                      <p className="text-lg text-gray-300 mb-2">Número:</p>
                      <p className="text-2xl font-mono">843685160</p>
                      <button
                        onClick={() => handleCopy('843685160', 'mpesa')}
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                        title="Copiar número"
                      >
                        {copiedMpesa ? (
                          <Check className="w-5 h-5 text-green-400" />
                        ) : (
                          <Copy className="w-5 h-5" />
                        )}
                      </button>
                    </div>
                  </div>
                </div>

                <div className="bg-green-900/30 p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <DollarSign className="text-green-400" />
                    E-mola
                  </h3>
                  <p className="text-gray-300 mb-4">
                    Para doar via E-mola, envie sua contribuição para:
                  </p>
                  <div className="space-y-2">
                    <div className="bg-green-950/50 p-4 rounded-lg">
                      <p className="text-lg text-gray-300 mb-2">Nome:</p>
                      <p className="text-xl font-semibold">Francisco Agostinho</p>
                    </div>
                    <div className="bg-green-950/50 p-4 rounded-lg relative group">
                      <p className="text-lg text-gray-300 mb-2">Número:</p>
                      <p className="text-2xl font-mono">870251917</p>
                      <button
                        onClick={() => handleCopy('870251917', 'emola')}
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                        title="Copiar número"
                      >
                        {copiedEmola ? (
                          <Check className="w-5 h-5 text-green-400" />
                        ) : (
                          <Copy className="w-5 h-5" />
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold mb-4">Agradecimento</h2>
              <p className="text-gray-300">
                Agradecemos imensamente sua contribuição para o desenvolvimento do cinema 
                moçambicano. Cada doação nos ajuda a continuar contando histórias 
                importantes e desenvolvendo talentos locais. Juntos, podemos fortalecer 
                a indústria cinematográfica de Moçambique.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DonatePage;