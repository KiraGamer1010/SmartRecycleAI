export const theoryDocument = {
  deliverable: "R2-A1-S6 Entrega diseño y plan de producción del Proyecto",
  project: "SMARTRECYCLEAI",
  authors: [
    "Juan Esteban Castiblanco",
    "Cristian Mauricio Muñoz",
    "Juan David Capera"
  ],
  course: "Machine Learning",
  university: "Universidad de Cundinamarca",
  campus: "Chía, Cundinamarca",
  date: "16/05/2026"
};

export const theoryStats = [
  { label: "Secciones académicas", value: "21" },
  { label: "Categorias iniciales", value: "8" },
  { label: "Fuentes de datos", value: "5" },
  { label: "Referencias", value: "10" }
];

export const mlTimeline = [
  {
    title: "Entendimiento del negocio",
    detail: "Alinear las soluciones técnicas con las necesidades reales de la organización."
  },
  {
    title: "Evaluación de datos",
    detail: "Analizar calidad, suficiencia y relevancia antes del entrenamiento."
  },
  {
    title: "Análisis de viabilidad",
    detail: "Determinar capacidad técnica, operativa y organizacional."
  },
  {
    title: "Ingeniería de datos",
    detail: "Seleccionar, limpiar, transformar y documentar datos."
  },
  {
    title: "MLOps",
    detail: "Automatización, monitoreo y control de versiones para producción."
  }
];

export const technologyGroups = [
  {
    title: "Backend",
    items: ["Python.", "FastAPI.", "PostgreSQL."]
  },
  {
    title: "Inteligencia Artificial",
    items: ["TensorFlow.", "PyTorch.", "OpenCV.", "Scikit-learn."]
  },
  {
    title: "Frontend",
    items: ["React.", "Vite.", "TailwindCSS."]
  },
  {
    title: "Infraestructura MLOps",
    items: ["Docker.", "GitHub Actions.", "MLflow.", "DVC."]
  }
];

export const datasetSources = [
  "Datasets públicos de residuos reciclables.",
  "Imágenes obtenidas mediante cámaras.",
  "Registros de clasificación manual.",
  "Bases de datos etiquetadas.",
  "Metadatos asociados a imágenes."
];

export const publicDatasets = [
  "TrashNet Dataset.",
  "TACO Dataset (Trash Annotations in Context).",
  "Waste Classification Dataset.",
  "Garbage Classification Dataset."
];

export const riskGroups = [
  {
    title: "Riesgos Técnicos",
    items: [
      "Sobreajuste del modelo.",
      "Bajo rendimiento en producción.",
      "Tiempo elevado de inferencia.",
      "Insuficiencia de datos."
    ]
  },
  {
    title: "Riesgos Organizacionales",
    items: [
      "Limitaciones presupuestales.",
      "Resistencia al cambio tecnológico.",
      "Falta de personal especializado."
    ]
  },
  {
    title: "Riesgos de Datos",
    items: [
      "Sesgo en datasets.",
      "Etiquetado incorrecto.",
      "Información incompleta."
    ]
  }
];

export const references = [
  "Kreuzberger, D., Kühl, N., & Hirschl, S. (2022). Machine Learning Operations (MLOps): Overview, Definition, and Architecture. IEEE Access. Disponible en: https://arxiv.org/abs/2205.02302",
  "ML-Ops.org. Machine Learning Operations. Disponible en: https://ml-ops.org/",
  "AWS. ¿Qué son las MLOps? Disponible en: https://aws.amazon.com/es/what-is/mlops/",
  "IBM. ¿Qué son las operaciones de machine learning (MLOps)? Disponible en: https://www.ibm.com/es-es/think/topics/mlops",
  "Google Cloud. What is MLOps? Disponible en: https://cloud.google.com/discover/what-is-mlops",
  "Sugimura, P., & Hartl, F. (2018). Building a Reproducible Machine Learning Pipeline. Disponible en: https://arxiv.org/abs/1810.04570",
  "Samuel, S., Löffler, F., & König-Ries, B. (2020). Machine Learning Pipelines: Provenance, Reproducibility and FAIR Data Principles. Disponible en: https://arxiv.org/abs/2006.12117",
  "Databricks. What is MLOps? Disponible en: https://www.databricks.com/blog/what-is-mlops",
  "Red Hat. What is MLOps? Disponible en: https://www.redhat.com/en/topics/ai/what-is-mlops",
  "Schmitt, M. (2023). Automated Machine Learning for Business Analytics. Disponible en: https://strathprints.strath.ac.uk/85263/1/Schmitt_ISA_2023_Intelliegent_systems_with_applications.pdf"
];

export const theorySections = [
  {
    id: "introduccion",
    number: "01",
    title: "Introducción",
    eyebrow: "Documento académico",
    paragraphs: [
      theoryDocument.deliverable,
      theoryDocument.project,
      "Autores: Juan Esteban Castiblanco, Cristian Mauricio Muñoz, Juan David Capera.",
      "Asignatura: Machine Learning.",
      "Universidad: Universidad de Cundinamarca.",
      "Sede: Chía, Cundinamarca.",
      "Fecha: 16/05/2026."
    ]
  },
  {
    id: "entendimiento-negocio-datos",
    number: "02",
    title: "Entendimiento del Negocio y los Datos",
    eyebrow: "ENTENDIMIENTO DEL NEGOCIO Y LOS DATOS",
    paragraphs: [
      "Según el enfoque CRISP-ML(Q) y las prácticas de MLOps, el entendimiento del negocio constituye una fase crítica debido a que permite alinear las soluciones técnicas con las necesidades reales de la organización.",
      "El proyecto busca solucionar problemáticas identificadas en sistemas tradicionales de reciclaje:",
      "Diversos estudios indican que los sistemas de Machine Learning permiten automatizar procesos complejos de clasificación y toma de decisiones mediante el reconocimiento de patrones en grandes volúmenes de datos."
    ],
    bullets: [
      "Clasificación incorrecta de residuos.",
      "Baja eficiencia en procesos manuales de separación.",
      "Contaminación cruzada entre residuos reciclables y no reciclables.",
      "Escasa automatización en centros de reciclaje.",
      "Dificultad para analizar patrones de generación de residuos."
    ]
  },
  {
    id: "objetivos-negocio",
    number: "03",
    title: "Objetivos de Negocio",
    eyebrow: "1. Objetivos de Negocio",
    paragraphs: [
      "El objetivo principal del proyecto SmartRecycleAI es desarrollar un sistema inteligente basado en Machine Learning y visión por computadora que permita clasificar residuos automáticamente, optimizando los procesos de reciclaje y reduciendo errores humanos en la separación de materiales."
    ]
  },
  {
    id: "objetivos-especificos",
    number: "04",
    title: "Objetivos Específicos",
    paragraphs: [
      "La implementación de prácticas MLOps permite garantizar automatización, monitoreo y mantenimiento continuo de modelos de Machine Learning en producción."
    ],
    bullets: [
      "Diseñar un modelo de Machine Learning capaz de identificar diferentes tipos de residuos reciclables.",
      "Mejorar la precisión en la clasificación automática mediante técnicas de visión computacional.",
      "Reducir errores humanos en procesos de separación manual.",
      "Optimizar tiempos de procesamiento de residuos.",
      "Facilitar la toma de decisiones mediante análisis de datos ambientales.",
      "Permitir escalabilidad futura mediante integración con tecnologías IoT y MLOps."
    ]
  },
  {
    id: "preguntas-clave",
    number: "05",
    title: "Preguntas Clave",
    eyebrow: "2. Preguntas Clave del Proyecto",
    paragraphs: [
      "Durante la fase de análisis se identificaron las principales preguntas que el sistema debe responder:",
      "Estas preguntas son fundamentales para transformar necesidades empresariales en objetivos medibles de Machine Learning."
    ],
    bullets: [
      "¿Qué tipo de residuo está siendo analizado?",
      "¿El residuo es reciclable o no reciclable?",
      "¿Cuál es el nivel de confianza de la clasificación?",
      "¿Qué materiales generan mayor tasa de error?",
      "¿Qué características visuales diferencian cada categoría?",
      "¿El sistema puede operar en tiempo real?",
      "¿Cómo reducir el sobreajuste y aumentar precisión?",
      "¿Qué impacto tiene la automatización sobre la eficiencia del reciclaje?"
    ]
  },
  {
    id: "variables-interes",
    number: "06",
    title: "Variables de Interés",
    paragraphs: [
      "Las variables utilizadas para el entrenamiento del modelo incluyen:",
      "La correcta selección de variables influye directamente en el rendimiento predictivo del modelo y en su capacidad de generalización."
    ],
    bullets: [
      "Tipo de material.",
      "Color dominante.",
      "Forma geométrica.",
      "Textura visual.",
      "Tamaño del objeto.",
      "Etiqueta de clasificación.",
      "Nivel de confianza del modelo.",
      "Tiempo de inferencia.",
      "Calidad de imagen."
    ]
  },
  {
    id: "evaluacion-datos",
    number: "07",
    title: "Evaluación de Datos",
    eyebrow: "3. Evaluación de Datos",
    paragraphs: [
      "La evaluación de datos consiste en analizar la calidad, suficiencia y relevancia de la información disponible antes del entrenamiento del modelo.",
      "La literatura de MLOps establece que los datos son uno de los pilares fundamentales del ciclo de vida de Machine Learning y deben tratarse como activos críticos del sistema."
    ]
  },
  {
    id: "fuentes-datos",
    number: "08",
    title: "Fuentes de Datos",
    eyebrow: "Fuentes de Datos Identificadas",
    paragraphs: [
      "Las fuentes consideradas para el proyecto son:",
      "Estos datasets son ampliamente utilizados en investigaciones académicas relacionadas con clasificación automática de residuos mediante Deep Learning."
    ],
    bullets: datasetSources,
    datasets: publicDatasets
  },
  {
    id: "calidad-datos",
    number: "09",
    title: "Calidad de Datos",
    eyebrow: "Calidad de los Datos",
    paragraphs: [
      "Se analizaron los siguientes criterios:",
      "Los problemas de calidad de datos pueden afectar directamente la precisión y confiabilidad del modelo predictivo."
    ],
    cards: [
      {
        title: "Integridad",
        body: "Se verificó que los datos contengan información suficiente para el entrenamiento y validación del modelo."
      },
      {
        title: "Consistencia",
        body: "Se comprobó uniformidad en etiquetas, nombres y categorías."
      },
      {
        title: "Precisión",
        body: "Se validó que cada imagen corresponda correctamente a su categoría."
      },
      {
        title: "Balance de Clases",
        body: "Se analizó la distribución de datos entre categorías para evitar sesgos."
      },
      {
        title: "Cantidad de Datos",
        body: "Se evaluó si existe volumen suficiente para entrenar modelos robustos sin sobreajuste."
      }
    ]
  },
  {
    id: "problemas-detectados",
    number: "10",
    title: "Problemas Detectados",
    paragraphs: [
      "Durante la evaluación inicial se identificaron posibles riesgos:",
      "Según investigaciones sobre reproducibilidad en Machine Learning, la calidad de los datos y la trazabilidad de transformaciones son esenciales para garantizar resultados confiables."
    ],
    bullets: [
      "Imágenes borrosas.",
      "Etiquetas incorrectas.",
      "Clases desbalanceadas.",
      "Datos duplicados.",
      "Diferencias de iluminación.",
      "Variaciones de ángulo y posición."
    ]
  },
  {
    id: "analisis-viabilidad",
    number: "11",
    title: "Análisis de Viabilidad",
    eyebrow: "4. Análisis de Viabilidad",
    paragraphs: [
      "El análisis de viabilidad permite determinar si el proyecto puede desarrollarse exitosamente desde el punto de vista técnico, operativo y organizacional.",
      "El proyecto es técnicamente viable debido a:",
      "Actualmente, tecnologías como TensorFlow y PyTorch son estándares ampliamente utilizados para aplicaciones industriales de Machine Learning.",
      "El sistema puede integrarse mediante:",
      "Además, el uso de APIs modernas facilita escalabilidad e integración con futuras plataformas industriales."
    ],
    groups: [
      {
        title: "Viabilidad Técnica",
        items: [
          "Disponibilidad de frameworks avanzados de IA.",
          "Existencia de datasets públicos.",
          "Disponibilidad de GPUs y servicios cloud.",
          "Compatibilidad con visión computacional.",
          "Amplio soporte para MLOps y automatización."
        ]
      },
      {
        title: "Viabilidad Operativa",
        items: [
          "Cámaras inteligentes.",
          "Sensores IoT.",
          "Aplicaciones web.",
          "Sistemas automatizados de clasificación."
        ]
      }
    ]
  },
  {
    id: "tecnologias-seleccionadas",
    number: "12",
    title: "Tecnologías Seleccionadas",
    paragraphs: [
      "Las prácticas modernas de MLOps permiten automatizar entrenamiento, despliegue y monitoreo continuo de modelos inteligentes."
    ],
    technologies: technologyGroups
  },
  {
    id: "riesgos-identificados",
    number: "13",
    title: "Riesgos Identificados",
    paragraphs: [
      "La literatura científica identifica la deuda técnica y la falta de reproducibilidad como problemas frecuentes en proyectos de Machine Learning."
    ],
    risks: riskGroups
  },
  {
    id: "estrategias-mitigacion",
    number: "14",
    title: "Estrategias de Mitigación",
    paragraphs: [
      "Para minimizar riesgos se implementarán las siguientes estrategias:",
      "Las metodologías MLOps recomiendan automatización, monitoreo y control de versiones para garantizar mantenibilidad y reproducibilidad."
    ],
    bullets: [
      "Aplicación de Data Augmentation.",
      "Validación cruzada.",
      "Monitoreo continuo del modelo.",
      "Versionamiento de datos y modelos.",
      "Documentación técnica detallada.",
      "Evaluaciones periódicas de precisión."
    ]
  },
  {
    id: "ingenieria-datos",
    number: "15",
    title: "Ingeniería de Datos",
    eyebrow: "INGENIERÍA DE DATOS",
    paragraphs: [
      "La selección de datos consiste en identificar información relevante para entrenar modelos predictivos confiables."
    ],
    timeline: mlTimeline
  },
  {
    id: "seleccion-datos",
    number: "16",
    title: "Selección de Datos",
    eyebrow: "1. Selección de Datos",
    paragraphs: [
      "El proyecto utilizará:",
      "Las categorías definidas son:",
      "Los datos deben cumplir con:",
      "La correcta selección de datos es determinante para reducir sesgos y mejorar capacidad predictiva."
    ],
    groups: [
      {
        title: "Datos Seleccionados",
        items: [
          "Imágenes de residuos reciclables.",
          "Imágenes de residuos orgánicos.",
          "Registros etiquetados manualmente.",
          "Metadatos de captura.",
          "Categorías clasificadas."
        ]
      },
      {
        title: "Categorías Iniciales",
        items: [
          "Plástico.",
          "Papel.",
          "Cartón.",
          "Vidrio.",
          "Metal.",
          "Orgánicos.",
          "Electrónicos.",
          "No reciclables."
        ]
      },
      {
        title: "Criterios de Selección",
        items: [
          "Alta calidad visual.",
          "Etiquetado correcto.",
          "Diversidad de escenarios.",
          "Balance entre categorías.",
          "Relevancia para el problema."
        ]
      }
    ]
  },
  {
    id: "limpieza-datos",
    number: "17",
    title: "Limpieza de Datos",
    eyebrow: "2. Limpieza de Datos",
    paragraphs: [
      "La limpieza de datos busca mejorar calidad y consistencia antes del entrenamiento.",
      "La limpieza de datos es esencial para reducir errores y mejorar precisión del modelo."
    ],
    cards: [
      {
        title: "Eliminación de Duplicados",
        body: "Se eliminarán imágenes repetidas para evitar sesgos."
      },
      {
        title: "Corrección de Etiquetas",
        body: "Se validarán categorías manualmente."
      },
      {
        title: "Eliminación de Datos Inválidos",
        body: "Se descartarán archivos corruptos o ilegibles."
      },
      {
        title: "Gestión de Valores Faltantes",
        body: "Se completarán o eliminarán registros incompletos."
      },
      {
        title: "Estandarización",
        body: "Se unificarán formatos y nombres de categorías."
      }
    ]
  },
  {
    id: "transformacion-datos",
    number: "18",
    title: "Transformación de Datos",
    eyebrow: "3. Transformación de Datos",
    paragraphs: [
      "La transformación prepara la información para maximizar rendimiento del modelo.",
      "Transformaciones aplicadas:",
      "Identificación de:",
      "Las transformaciones permiten mejorar generalización y reducir sobreajuste del modelo."
    ],
    groups: [
      {
        title: "Técnicas Aplicadas",
        items: [
          "Normalización: Escalamiento de valores numéricos.",
          "Redimensionamiento: Unificación de tamaño de imágenes.",
          "Codificación de Etiquetas: Conversión de categorías a valores numéricos."
        ]
      },
      {
        title: "Data Augmentation",
        items: [
          "Rotación.",
          "Reflejo horizontal.",
          "Zoom.",
          "Variación de brillo.",
          "Recorte."
        ]
      },
      {
        title: "Extracción de Características",
        items: [
          "Bordes.",
          "Texturas.",
          "Colores.",
          "Formas geométricas."
        ]
      }
    ]
  },
  {
    id: "documentacion-transformaciones",
    number: "19",
    title: "Documentación de Transformaciones",
    eyebrow: "4. Documentación de Transformaciones",
    paragraphs: [
      "La documentación garantiza reproducibilidad y trazabilidad del proyecto.",
      "Según estándares MLOps, todas las decisiones sobre datos y modelos deben registrarse formalmente para asegurar mantenimiento y auditoría futura.",
      "La documentación permite:",
      "La reproducibilidad es considerada uno de los pilares fundamentales de los sistemas modernos de Machine Learning."
    ],
    groups: [
      {
        title: "Información Documentada",
        items: [
          "Fuente del dataset.",
          "Fecha de adquisición.",
          "Transformaciones aplicadas.",
          "Herramientas utilizadas.",
          "Parámetros de entrenamiento.",
          "Versiones de librerías.",
          "Métricas obtenidas."
        ]
      },
      {
        title: "Importancia de la Documentación",
        items: [
          "Reproducir experimentos.",
          "Facilitar mantenimiento.",
          "Detectar errores.",
          "Validar resultados.",
          "Garantizar trazabilidad."
        ]
      }
    ]
  },
  {
    id: "conclusion",
    number: "20",
    title: "Conclusión",
    eyebrow: "CONCLUSIÓN",
    paragraphs: [
      "La fase de entendimiento del negocio y los datos permitió establecer bases sólidas para el desarrollo del sistema inteligente de reciclaje SmartRecycleAI. Se identificaron los objetivos principales, preguntas críticas, riesgos y necesidades técnicas del proyecto.",
      "Asimismo, la ingeniería de datos permitió estructurar adecuadamente la información necesaria para entrenar modelos de Machine Learning confiables, reduciendo problemas de calidad y aumentando la capacidad predictiva del sistema.",
      "Todo este proceso garantiza que el desarrollo posterior del modelo esté alineado tanto con las necesidades del negocio como con buenas prácticas de ciencia de datos y MLOps."
    ]
  },
  {
    id: "referencias-bibliograficas",
    number: "21",
    title: "Referencias Bibliográficas",
    eyebrow: "REFERENCIAS BIBLIOGRÁFICAS",
    references
  }
];
