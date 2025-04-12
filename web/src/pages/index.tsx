import { useState } from "react";
import Image from "next/image";
import { User, Flag, MessageCircleMore, Users, Github, Calendar } from "lucide-react";
import Resultado from "./componentes/Resultado";
import { motion } from "framer-motion";
import { useRouter } from "next/router";

export default function Home() {

  interface UserProfile {
    nome: string;
    imagem: string;
    localizacao: string | null;
    bio: string | null;
    seguidores: number | null;
    repositorios: number | null;
    data_criacao: string | null;
    resposta: string;
  }

  const [value, setValue] = useState("");
  const [erro, setErro] = useState(false);
  const [erroMessage, setErroMessage] = useState("");
  const [data, setData] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(false);

  const navigate = useRouter();

  const handleClick = () => {
    navigate.push("https://github.com/victorlima11/AnalisadorGitHub")
  }

  const handleAnalise = async () => {
    setErro(false);
    if (!value || value == "") {
      setErro(true);
      setErroMessage("Por favor, insira um usuário.");
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/${value}`)
      const data = await response.json();

      if (!response.ok) {
        setErro(true);
        setLoading(false);
        setErroMessage("Usuário não encontrado.");
        return;
      }

      setLoading(false);
      setData(data);
      console.log(data);
    } catch (error) {
      setErroMessage("Erro ao buscar dados do usuário.");
      setErro(true);
    }

  };


  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="text-4xl font-bold">Analisador de Github</h1>
      <h2 className="font-light">Veja o que uma IA tem a dizer sobre o seu perfil.</h2>
      <div className="flex flex-col items-center justify-center mt-5">
        <h1>Insira um usuário para análise.</h1>
        <div className="flex flex-row items-center justify-center mt-5">
          <input
            type="text"
            placeholder="Digite o nome do usuário"
            className="border-2 border-gray-300 rounded-lg p-2"
            required
            onChange={(e) => setValue(e.target.value)}
          />
          <button onClick={handleAnalise} className="ml-2 bg-blue-500 text-white rounded-lg p-2 hover:cursor-pointer">
            Analisar
          </button>
        </div>
      </div>
      <div className="flex flex-col items-center justify-center mt-5">
        {erro && (
          <div className="bg-red-500 text-white rounded-lg p-2 mb-2">
            <p>{erroMessage}</p>
          </div>
        )}
        {loading && (
          <div className="flex flex-row gap-2 mb-2">
            <div className="w-4 h-4 rounded-full bg-blue-500 animate-bounce"></div>
            <div
              className="w-4 h-4 rounded-full bg-blue-500 animate-bounce [animation-delay:-.3s]"
            ></div>
            <div
              className="w-4 h-4 rounded-full bg-blue-500 animate-bounce [animation-delay:-.5s]"
            ></div>
          </div>
        )}
        {data && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="bg-gray-100 text-gray-700 rounded-2xl p-6 max-w-2xl shadow-lg hover:shadow-2xl transition-shadow duration-300">
            <div className="flex flex-row items-center justify-start gap-6">
              <Image
                className="rounded-2xl"
                src={data.imagem}
                width={120}
                height={120}
                alt="Avatar do Usuário"
              />
              <div className="flex flex-col items-start justify-center space-y-2">
                <div className="flex flex-row items-center gap-2 text-lg font-semibold">
                  <User className="" />
                  <p>{data.nome}</p>
                </div>
                {data.localizacao ? (
                  <div className="flex flex-row items-center gap-2">
                    <Flag className="" />
                    <p>{data.localizacao}</p>
                  </div>
                ) : (
                  <p className="text-gray-400">Localização não informada</p>
                )}
              </div>
            </div>
            <div className="mt-4 space-y-2">
              {data.seguidores ? (
                <div className="flex items-center gap-2">
                  <Users className="" />
                  <p>Seguidores: {data.seguidores}</p>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Users className="" />
                  <p>Não possui seguidores</p>
                </div>
              )}
              {data.repositorios ? (
                <div className="flex items-center gap-2">
                  <Github className="" />
                  <p>Repositórios: {data.repositorios}</p>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Github className="" />
                  <p>Não possui repositórios públicos</p>
                </div>
              )}
              {data.data_criacao ? (
                <div className="flex items-center gap-2">
                  <Calendar className="" />
                  <p>Data de Criação: {new Date(data.data_criacao).toLocaleDateString("pt-BR")}</p>
                </div>
              ) : (
                <p className="text-gray-400">Data de criação não informada</p>
              )}
            </div>
            <div className="mt-6">
              <div className="bg-gray-800 text-white rounded-lg p-4 mt-2">
                <Resultado markdown={data.resposta} />
              </div>
            </div>
          </motion.div>
        )}
        <div
          className="fixed bottom-6 right-6 p-3 bg-black text-white rounded-full shadow-lg hover:bg-white hover:text-black transition duration-300 cursor-pointer"
          onClick={handleClick}>
          <Github size={32} />
        </div>
      </div>
    </div>
  );
}
