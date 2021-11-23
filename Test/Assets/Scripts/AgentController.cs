using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Agents
{
    public List<Vector3> positions;
}
public class AgentController : MonoBehaviour
{
    [SerializeField] string url;
    [SerializeField] string testEP;
    [SerializeField] string configEP;
    [SerializeField] private string updateEP;
    [SerializeField] private string updateOrganizingAgentsEP;
    [SerializeField] private string updateBoxAgentsEP;
    [SerializeField] int numAgents;
    [SerializeField] int numBoxes;
    [SerializeField] int width;
    [SerializeField] int height;
    [SerializeField] private GameObject organizingAgentPrefab;
    [SerializeField] private GameObject boxAgentPrefab;
    [SerializeField] private float updateDealy;
    [SerializeField] GameObject floor;

    Agents oAgents, bAgents;
    GameObject[] organizingAgents, boxAgents;
    private float updateTime = 0;

    // Start is called before the first frame update
    void Start()
    {
        organizingAgents = new GameObject[numAgents];
        boxAgents = new GameObject[numBoxes];

        floor.transform.localScale = new Vector3((float) width / 10, 1, (float) height / 10);
        floor.transform.localPosition = new Vector3((float) width / 2 - 0.5f, 0, (float) height / 2 - 0.5f);
        
        for (int i = 0; i < numAgents; i++)
        {
            organizingAgents[i] = Instantiate(organizingAgentPrefab, Vector3.up, Quaternion.identity);
        }
        
        for (int i = 0; i < numBoxes; i++)
        {
            boxAgents[i] = Instantiate(boxAgentPrefab, Vector3.up, Quaternion.identity);
        }
        
        StartCoroutine(SendConfig()); 
    }

    // Update is called once per frame
    void Update()
    {
        if (updateTime > updateDealy)
        {
            StartCoroutine(UpdateSimulation());
            //MoveAgents();
            updateTime = 0;
        }

        updateTime += Time.deltaTime;
    }

    IEnumerator TestAPI()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + testEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
        }
        else
        {
            Debug.Log(www.error);
        }
    }
    
    IEnumerator SendConfig()
    {
        WWWForm form = new WWWForm();
        form.AddField("numAgents", numAgents.ToString());
        form.AddField("numBoxes", numBoxes.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        
        UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            StartCoroutine(GetOrganizingData());
            StartCoroutine(GetBoxData());
        }
        else
        {
            Debug.Log(www.error);
        }
    }
    
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetOrganizingData());
            StartCoroutine(GetBoxData());
        }
    }

    IEnumerator GetOrganizingData()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateOrganizingAgentsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        { 
            oAgents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            MoveOrganizingAgents();
        }
    }
    
    IEnumerator GetBoxData()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateBoxAgentsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            bAgents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            MoveBoxAgent();
        }
    }

    void MoveOrganizingAgents()
    {
        for (int i = 0; i < numAgents; i++)
        {
            organizingAgents[i].transform.position = oAgents.positions[i];
        }
    }

    void MoveBoxAgent()
    {
        for (int i = 0; i < numBoxes; i++)
        {
            boxAgents[i].transform.position = bAgents.positions[i];
        }
    }
}
